"""
This module holds the GraphQL schema for the app.
"""

from graphene import (
    ObjectType, String, Boolean, Field, Int, List, Schema, Mutation
)
from graphene_sqlalchemy import SQLAlchemyObjectType
from .models import Task
from .database import database


# GraphQL Object Type for Task
class TaskType(SQLAlchemyObjectType):
    class Meta:
        model = Task


# Query: Fetch Data
class Query(ObjectType):
    tasks = List(TaskType)
    task = Field(TaskType, id=Int(required=True))

    def resolve_tasks(parent, info):
        # Fetch all tasks
        return Task.query.all()

    def resolve_task(parent, info, id):
        # Fetch a single task by ID
        return Task.query.get(id)


# Mutation: Create, Update, Delete Tasks
class CreateTask(Mutation):
    class Arguments:
        title = String(required=True)
        status = String()
        tags = List(String)

    task = Field(lambda: TaskType)

    def mutate(parent, info, title=None, status="pending", tags=None):
        task = Task(title=title, status=status, tags=tags or [])
        database.session.add(task)
        database.session.commit()
        return CreateTask(task=task)


class UpdateTask(Mutation):
    class Arguments:
        id = Int(required=True)
        title = String()
        description = String()
        is_completed = Boolean()

    task = Field(lambda: TaskType)

    def mutate(
        parent, info, id, title=None, description=None, is_completed=None
    ):
        task = Task.query.get(id)
        if not task:
            raise Exception("Task not found")
        if title:
            task.title = title
        if description:
            task.description = description
        if is_completed is not None:
            task.is_completed = is_completed
        database.session.commit()
        return UpdateTask(task=task)


class DeleteTask(Mutation):
    class Arguments:
        id = Int(required=True)

    success = Boolean()

    def mutate(parent, info, id):
        task = Task.query.get(id)
        if not task:
            return DeleteTask(success=False)
        database.session.delete(task)
        database.session.commit()
        return DeleteTask(success=True)


# Root Mutation
class Mutation(ObjectType):
    create_task = CreateTask.Field()
    update_task = UpdateTask.Field()
    delete_task = DeleteTask.Field()


# Combine Query and Mutation into a Schema
schema = Schema(query=Query, mutation=Mutation)
