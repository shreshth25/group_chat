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
    ADMIN+'/create-admin': AdminController.CreateAdmin(),
    ADMIN+'/create-user':AdminController.CreateUser(),
    ADMIN+'/update-user':AdminController.UpdateUser(),
    ADMIN+'/get-users':AdminController.Users(),
    ADMIN+'/get-chat-groups':AdminController.chat_groups(),

    #Authentication
    "/login":AuthController.Login(),
    "/logout":AuthController.Logout(),

    #users
    "/users-list": GroupController.UsersList(),
    "/create-group": GroupController.CreateGroup(),
    "/chat-groups-list": GroupController.GroupList(),
    "/search-group": GroupController.SearchGroup(),
    "/delete-group": GroupController.DeleteGroup(), #tobedone
    "/add-user": GroupController.AddUser(),

    #messages
    "/create-message": MessageController.CreateMessage(),
    "/messages-list": MessageController.MessageList(),

    #like
    "/create-like": LikeController.CreateLike(),
}
