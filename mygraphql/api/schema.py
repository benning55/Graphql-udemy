import graphene
from graphene import relay
from graphene_django.filter import DjangoFilterConnectionField
from graphene_django.types import DjangoObjectType
from graphql_jwt.decorators import login_required
from graphql_relay import from_global_id

from api.models import Movies, Director
import graphql_jwt


class MovieType(DjangoObjectType):
    class Meta:
        model = Movies

    movie_age = graphene.String()

    def resolve_movie_age(self, info):
        return "Old movie" if self.year < 2000 else "New Movie"


class DirectorType(DjangoObjectType):
    class Meta:
        model = Director


# just for relay implementation
class MovieNode(DjangoObjectType):
    class Meta:
        model = Movies
        filter_fields = {
            'title': ['exact', 'icontains', ],
            'year': ['exact', ]
        }
        interfaces = (relay.Node, )


class Query(graphene.ObjectType):
    all_movies2 = DjangoFilterConnectionField(MovieNode) # relray type
    all_movies = graphene.List(MovieType)
    movie = graphene.List(MovieType, id=graphene.Int(), title=graphene.String())
    movie2 = relay.Node.Field(MovieNode)

    all_directors = graphene.List(DirectorType)

    @login_required
    def resolve_all_movies(self, info, **kwargs):
        return Movies.objects.all()

    # def resolve_all_movies(self, info, **kwargs):
    #     user = info.context.user
    #     if not user.is_authenticated:
    #         raise Exception('Auth credential were not provided')
    #     return Movies.objects.all()

    def resolve_movie(self, info, **kwargs):
        id = kwargs.get('id')
        title = kwargs.get('title')

        if id is not None:
            print("test")
            return Movies.objects.filter(id=id)

        if title is not None:
            return Movies.objects.filter(title__contains=title) if len(Movies.objects.filter(title__contains=title)) > 0 else None

        return None

    def resolve_all_directors(self, info, **kwargs):
        return Director.objects.all()


class MovieCreateMutation(graphene.Mutation):
    class Arguments:
        title = graphene.String(required=True)
        year = graphene.Int(required=True)

    movie = graphene.Field(MovieType)

    def mutate(self, info, title, year):
        movie = Movies.objects.create(
            title=title,
            year=year
        )

        return MovieCreateMutation(movie=movie)


class MovieUpdateMutation(graphene.Mutation):
    class Arguments:
        title = graphene.String()
        year = graphene.Int()
        id = graphene.Int()

    movie = graphene.Field(MovieType)

    def mutate(self, info, id, title, year):
        movie = Movies.objects.get(pk=id)
        if title is not None:
            movie.title = title
        if year is not None:
            movie.year = year

        movie.save()

        return MovieUpdateMutation(movie=movie)


class MovieUpdateMutationRelray(relay.ClientIDMutation):
    class Input:
        title = graphene.String()
        id = graphene.ID(required=True)

    movie = graphene.Field(MovieType)

    @classmethod
    def mutate_and_get_payload(cls, root, info, id, title):
        movie = Movies.objects.get(pk=from_global_id(id)[1])
        if title is not None:
            movie.title = title
        movie.save()

        return MovieUpdateMutationRelray(movie=movie)


class MovieDeleteMutation(graphene.Mutation):
    class Arguments:
        id = graphene.Int()

    movie = graphene.Field(MovieType)

    def mutate(self, info, id):
        movie = Movies.objects.get(pk=id)
        movie.delete()

        return MovieDeleteMutation(movie=None)


class Mutation:
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    create_movie = MovieCreateMutation.Field()
    update_movie = MovieUpdateMutation.Field()
    update_movie2 = MovieUpdateMutationRelray.Field()
    delete_movie = MovieDeleteMutation.Field()
