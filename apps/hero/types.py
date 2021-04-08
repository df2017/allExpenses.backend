import graphene
from graphene_django import DjangoObjectType
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from .models import Hero
from graphene import relay, ObjectType
from graphene_django.filter import DjangoFilterConnectionField
from django.db.models import Q
from graphql import GraphQLError
import json
import graphql_social_auth


class HeroType(DjangoObjectType):
    class Meta:
        model = Hero
        filter_fields = ['name', 'gender', 'movie']
        interfaces = (relay.Node, )

class Query(graphene.ObjectType):
    #heroes = graphene.List(HeroType)
    all_heroes = DjangoFilterConnectionField(HeroType)

    links = graphene.List(
        HeroType,
        search=graphene.String(),
        first=graphene.Int(),
        skip=graphene.Int(),
        filter_column=graphene.String(),
    )

    def resolve_all_heroes(self, info, gender=None):
        if not info.context.user.is_authenticated:
            print('INFO: ', info.context.user)
            raise GraphQLError('Error login')
        else:
            return Hero.objects.filter(gender=gender)

    def resolve_links(self, info, search=None, first=None, skip=None, filter_column=None):
        qs = Hero.objects.all()

        if not info.context.user.is_authenticated:
            raise Exception('Not logged in!')
        else:
            if search:
                filter = (
                        Q(name__icontains=search) |
                        Q(movie__icontains=search)
                )
                qs = qs.filter(filter)

            if filter_column:
                param = eval(filter_column)
                qs = qs.filter(**param)

            if skip:
                qs = qs[skip:]

            if first:
                qs = qs[:first]



            return qs



class CreateHero(graphene.Mutation):

  class Arguments:
    name = graphene.String(required=True)
    gender = graphene.String(required=True)
    movie = graphene.String(required=True)

  hero = graphene.Field(HeroType)

  def mutate(self, info, name, gender, movie):
    hero = Hero.objects.create(
      name = name,
      gender = gender,
      movie = movie,
    )
    hero.save()

    return CreateHero(hero=hero)

class Mutation(graphene.ObjectType):
    create_hero = CreateHero.Field()