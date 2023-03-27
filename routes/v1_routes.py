from controllers import (
    AdminController,
    AuthController,
    HealthController,
    MessageController,
)
from controllers import GroupController, FakerController, LikeController
USER_PRIFIX = "/users"
ADMIN = '/admin'


# API Routes
V1Routes = {
    # Health Routes
    "/health": HealthController.AppHealthCheck(),

    #Admin routes
    ADMIN+'/create_admin': AdminController.CreateAdmin(),
    ADMIN+'/create_user':AdminController.CreateUser(),
    ADMIN+'/update_user':AdminController.UpdateUser(), #tobedone
    ADMIN+'/get_users':AdminController.Users(),
    ADMIN+'/get_chat_groups':AdminController.chat_groups(),

    #Authentication
    "/login":AuthController.Login(),
    "/logout":AuthController.Logout(),

    #users
    "/users-list": GroupController.UsersList(),
    "/create-group": GroupController.CreateGroup(),
    "/chat_groups-list": GroupController.GroupList(),
    "/search-group": GroupController.SearchGroup(),
    "/delete-group": GroupController.GroupList(), #tobedone
    "/add-user": GroupController.AddUser(),

    #messages
    "/create-message": MessageController.CreateMessage(),
    "/messages-list": MessageController.MessageList(),

    #like
    "/create-like": LikeController.CreateLike(),
}
