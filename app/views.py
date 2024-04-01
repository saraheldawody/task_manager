from rest_framework.views import APIView 
from rest_framework.response import Response 
from rest_framework.permissions import IsAuthenticated , AllowAny
from django.contrib.auth import get_user_model
from rest_framework import exceptions
from rest_framework.decorators import parser_classes
from rest_framework.parsers import FileUploadParser
from django.http import HttpResponse
from .models import task, related_tasks
from .serializer import TaskSerializer
from rest_framework import serializers
class create_task(APIView):
    permission_classes = (AllowAny, ) 

    def post(self, request):
        if ('title' not in  request.data.keys()) or ('description' not in request.data.keys()):
            raise exceptions.ValidationError("Title and Description are required.")
        
        else:
            title = request.data['title']
            description = request.data['description']
            if task.objects.filter(title=title).first() is None:
                newTask = task.objects.create(title=title,description=description,status="New")
                newTask.save()
                return Response({'message':'Task '+title+' created Successfully'})
            else:
                raise exceptions.ValidationError("This Task already Exist.")

class get_all_tasks(APIView):
    permission_classes = (AllowAny, ) 

    def get(self, request):
        tasks = task.objects.all()

        if tasks.count() < 1:
            raise exceptions.ValidationError("There's no tasks to review")
        else:
            return Response({'data':TaskSerializer(tasks,many=True).data})


class proceed(APIView):
    permission_classes = (AllowAny, ) 

    def post(self, request):
        tasks = task.objects.all()
        if 'task_title' in request.data.keys():
            task_title = request.data['task_title']
            if task_title is None:
                raise exceptions.ValidationError("Please Provide the task title.")
            else:
                task_req = task.objects.filter(title=task_title).first()
                if task_title is None:
                    raise exceptions.ValidationError("Task "+task_title+" is noe Exist.")
                else:
                    if task_req.status == 'New':
                        task_req.status = 'In Progress'
                        task_req.save()
                        return Response({'message': 'Task '+task_req.title+' had been moved to In Progress Status'})
                    elif task_req.status == 'In Progress':
                        task_req.status = 'Done'
                        task_req.save()
                        return Response({'message': 'Task '+task_req.title+' had been moved to Done Status'})
                    else:
                        raise exceptions.ValidationError("Task "+task_title+" is already Done.")
        elif 'task_id' in request.data.keys():
            task_id = request.data['task_id']
            if task_id is None:
                raise exceptions.ValidationError("Please Provide the task ID.")
            else:
                task_req = task.objects.filter(id=task_id).first()
                if task_id is None:
                    raise exceptions.ValidationError("Task "+task_id+" is noe Exist.")
                else:
                    if task_req.status == 'New':
                        task_req.status = 'In Progress'
                        task_req.save()
                        return Response({'message': 'Task '+task_req.title+' had been moved to In Progress Status'})
                    elif task_req.status == 'In Progress':
                        task_req.status = 'Done'
                        task_req.save()
                        return Response({'message': 'Task '+task_req.title+' had been moved to Done Status'})
                    else:
                        raise exceptions.ValidationError("Task "+task_req.title+" is already Done.")
        else:
            raise exceptions.ValidationError("Please Provide Task Title or Task ID.")
        
class update_task(APIView):
    permission_classes = (AllowAny, ) 

    def post(self,request, id):
        if task.objects.filter(id=id).first() is None:
            raise exceptions.ValidationError("There's no task under this ID.")
        else:
            task_req = task.objects.get(id=id)
            if task_req.status == 'Done':
                raise exceptions.ValidationError('This Task is already "Done" you can not update it anymore.')
            if ('title'  in  request.data.keys()):
                title = request.data['title']
                if (task.objects.filter(title=title).first() is None):
                    if title is not None:
                        task_req.title = title
                else:
                    raise exceptions.ValidationError("This Task already Exist")
            if ('description'  in request.data.keys()):
                description = request.data['description']
                if description is not None:
                    task_req.description = description
            task_req.save()
            return Response({'message': 'The task has been updated'})

class link_tasks(APIView):
    permission_classes = (AllowAny, ) 

    def post(self, request):
        if ('task_one_id' in request.data.keys()) and ('task_two_id' in request.data.keys()):
            task1_id = request.data['task_one_id']
            task2_id = request.data['task_two_id']
            if (task1_id is None) or (task2_id is None):
                raise exceptions.ValidationError("task_one_id and task_two id are required to link between two tasks.")
            else:
                errors=[]
                if task.objects.filter(id=task1_id).first() is None:
                    errors.append("the provided task ID = "+str(task1_id)+" is not exist")
                if task.objects.filter(id=task2_id).first() is None:
                    errors.append("the provided task ID = "+str(task2_id)+" is not exist")
                if len(errors) > 0:
                    raise exceptions.ValidationError(errors)
                task_one = task.objects.get(id=task1_id)
                task_two = task.objects.get(id=task2_id)
                if  not (task_one.status == 'In Progress'):
                    errors.append("Task with ID = "+str(task1_id)+" is not In Progress so it can not be linked with any task.")
                if  not (task_two.status == 'In Progress'):
                    errors.append("Task with ID = "+str(task2_id)+" is not In Progress so it can not be linked with any task.")
                if len(errors) > 0:
                    raise exceptions.ValidationError(errors)
                if (related_tasks.objects.filter(TaskOne=task_one)) or (related_tasks.objects.filter(TaskTwo=task_one)):
                    errors.append("Task with ID = "+str(task1_id)+" is already related to another task")
                if (related_tasks.objects.filter(TaskOne=task_two)) or (related_tasks.objects.filter(TaskTwo=task_two)):
                    errors.append("Task with ID = "+str(task2_id)+" is already related to another task")
                if len(errors) > 0:
                    raise exceptions.ValidationError(errors)
                new_link = related_tasks.objects.create(TaskOne=task_one,TaskTwo=task_two)
                new_link.save()
                return Response({'message':'The two tasks had been linked together successfully.'})
        else:
            raise exceptions.ValidationError("task_one_id and task_two id are required to link between two tasks.")
        
class get_task(APIView):
    permission_classes = (AllowAny, ) 

    def get(self, request, id):
        if  task.objects.filter(id=id).first() is None:
            raise exceptions.ValidationError("This Id is not exist")
        else:
            task_req = task.objects.get(id=id)
            # case 1 "the task is linked to another task"
            if (related_tasks.objects.filter(TaskOne=task_req).first()) is not None: 
                link = related_tasks.objects.filter(TaskOne=task_req).first()
                content={
                    'message':"The requested task is linked to another one",
                    'task one': TaskSerializer(link.TaskOne).data,
                    'task two':TaskSerializer(link.TaskTwo).data
                }
                return Response(content)
            elif (related_tasks.objects.filter(TaskTwo=task_req).first()) is not None:
                link = related_tasks.objects.filter(TaskTwo=task_req).first()
                content={
                    'message':"The requested task is linked to another one",
                    'task one': TaskSerializer(link.TaskOne).data,
                    'task two':TaskSerializer(link.TaskTwo).data
                }
                return Response(content)
            else:
                # case 2 " the task is not linked"
                content={
                    'message':"The requested task is not linked to any other task.",
                    'task one': TaskSerializer(task_req).data
                    }
                return Response(content)







