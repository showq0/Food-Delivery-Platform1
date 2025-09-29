

# Feature1 APIs

**register** : http://127.0.0.1:5000/register

**login** : http://127.0.0.1:5000/login

**profile** <small>need access_token</small>: http://127.0.0.1:5000/profile

# Feature2 APIs

**user place order**: http://127.0.0.1:5000/order/menu

**track order**: http://127.0.0.1:5000/order/order/\<int:order_id>

**change status**:http://127.0.0.1:5000/order/order-status/\<int:order_id>

# Feature3 APIs

**driver send location**: http://127.0.0.1:5000/location/send/\<int:order_id>

**customer track location**: http://127.0.0.1:5000/location/track/\<int:order_id>

# Feature4 APIs

**order from resturant**: http://127.0.0.1:5000/notification/menu/\<int:restaurant_id>

**dashboard to see notification**: http://127.0.0.1:5000/notification/\<int:restaurant_id>

# Feature5 APIs

**agents**: http://127.0.0.1:5000/chat/agents

**chat room**: http://127.0.0.1:5000/chat/chat_room\<int:caht_id>

# Feature6 APIs

**get notification announcement**:http://127.0.0.1:5000/announcement/

**add announcement**:http://127.0.0.1:5000/announcement/add

# Feature7 APIs

**to upload image and get uploaded** :http://127.0.0.1:5000/image_pros
