from flask import Blueprint, request, jsonify
from app.controllers.user_story_controller import UserStoryController

user_story_routes = Blueprint('user_story_routes', __name__)
controller = UserStoryController()

@user_story_routes.route('/user-stories', methods=['GET'])
def list_user_stories():
    return controller.list_user_stories()

@user_story_routes.route('/user-stories/generate', methods=['POST'])
def generate_user_story_ia():
    return controller.generate_user_story_ia()

@user_story_routes.route('/user-stories', methods=['POST'])
def create_user_story_json():
    if request.is_json:
        return controller.create_user_story_json()
    else:
        return controller.create_user_story()

@user_story_routes.route('/user-stories/<int:user_story_id>/generate-tasks', methods=['POST'])
def generate_tasks(user_story_id):
    return controller.generate_tasks(user_story_id)

@user_story_routes.route('/user-stories/<int:user_story_id>/tasks', methods=['GET'])
def tasks_for_user_story(user_story_id):
    return controller.tasks_for_user_story(user_story_id) 