all_users_with_roles_query = '''SELECT 
    id,
    name,
    email,
    CASE
        WHEN is_admin = 1 THEN 'admin'
        ELSE 'user'
    END AS 'role'
FROM
    users'''

all_chat_groups_query='''SELECT 
    chat_groups.name AS 'group_name', users.name AS 'created_by'
FROM
    chat_groups
        JOIN
    users ON users.id = chat_groups.created_by where chat_groups.is_deleted = 0
'''

logged_out_query='''
    INSERT INTO
    blocked_tokens
    (user_id, token, is_deactivated, created_at)
    values
    (:user_id, :token, :is_deactivated, :created_at)
'''

check_if_logged_out='''
    SELECT id FROM
    blocked_tokens
    WHERE token= :token and is_deactivated=1
'''

user_list_query='''
    SELECT 
    id, name, email
FROM
    users
WHERE
    is_admin = 0 AND id != :id
'''


create_group_query = '''
INSERT INTO 
chat_groups 
(name, created_by, created_at, updated_at) 
VALUES 
(:name, :created_by, :current_datetime,:current_datetime)
'''

user_group_query = '''
SELECT *, "You" as 'creator' from chat_groups where created_by = :user_id and is_deleted = 0
UNION
SELECT g.*, u.name as 'creator' FROM group_users
join chat_groups as g on g.id = group_users.group_id
join users as u on u.id = g.created_by
where group_users.user_id = :user_id and g.is_deleted = 0
'''

check_if_user_can_like_message_query='''
SELECT 
    m.id
FROM
    chat_groups
JOIN messages as m on m.group_id = chat_groups.id
WHERE
    chat_groups.created_by= :user_id and m.id= :message_id and chat_groups.is_deleted = 0
UNION SELECT 
    m.id
FROM
    group_users
        JOIN
    chat_groups AS g ON g.id = group_users.group_id
        JOIN
    users AS u ON u.id = g.created_by
        JOIN
    messages AS m ON m.group_id = g.id
WHERE
    group_users.user_id= :user_id and m.id= :message_id and g.is_deleted = 0
'''

already_liked_query = '''
SELECT id 
from 
likes 
where 
message_id= :message_id and created_by= :user_id
'''

insert_liked_query = '''
Insert into 
likes 
(message_id, created_by, created_at, updated_at)
values 
(:message_id, :user_id, :current_datetime,:current_datetime)
'''

user_group_search_query='''
SELECT *, "You" as 'creator' from chat_groups where created_by = {} and is_deleted = 0 and name like "%{}%"
UNION
SELECT g.*, u.name as 'creator' FROM group_users
join chat_groups as g on g.id = group_users.group_id
join users as u on u.id = g.created_by
where group_users.user_id = {} and g.name like "%{}%" and g.is_deleted = 0
'''