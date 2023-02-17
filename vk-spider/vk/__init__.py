from pprint import pprint

import datetime
import vk_api


token = ""
group_id_root = 28905875

# Авторизуемся с помощью access token
vk_session = vk_api.VkApi(token=token)
vk = vk_session.get_api()

screen_name = (vk.groups.getById(group_id=group_id_root)[0]['screen_name'])

group_id_root = -group_id_root

def get_group_posts(group_id):
    all_posts = []
    offset = 0
    count = 100

    # Calculate the start time for the two-year period
    two_years_ago = datetime.datetime.now() - datetime.timedelta(days=365*2)
    start_time = int(two_years_ago.timestamp())

    while True:
        # Get the next batch of posts
        posts = vk.wall.get(owner_id=group_id, count=count, offset=offset, start_time=start_time)

        # If no more posts are available, break out of the loop
        if len(posts['items']) == 0:
            break

        # Process the posts in this batch
        for post in posts['items']:
            date = datetime.datetime.fromtimestamp(post['date'])
            id = post['id']
            post_link = f'https://vk.com/{screen_name}?w=wall{group_id_root}_{id}'
            post_data = {
                'post_id': post['id'],
                'text': post['text'],
                'likes': post['likes']['count'],
                'reposts': post['reposts']['count'],
                'views': post['views']['count'],
                'date': date,
                'link': post_link
            }

            if is_promoted_post(post_data):
                all_posts.append(post_data)
                pprint(post_data)

        # If the oldest post in this batch is older than two years, exit the loop
        oldest_post_date = datetime.datetime.fromtimestamp(posts['items'][-1]['date'])
        if oldest_post_date < two_years_ago:
            break

        # Increase the offset to retrieve the next batch of posts
        offset += count

    pprint(all_posts)
    return all_posts

def get_comments_of_post(group_id, post_id):
    # Get the comments for the post
    comments = vk.wall.getComments(owner_id=group_id, post_id=post_id, count=100, thread_items_count=10, need_likes=1, extended=1)

    # Create an empty list to hold the comments
    all_comments = []

    # Keep fetching more comments until we have them all
    while comments['items']:
        # Append the comments to the list
        all_comments.extend(comments['items'])
        # Get the next batch of comments
        comments = vk.wall.getComments(
            owner_id=group_id,
            post_id=post_id,
            count=100,
            thread_items_count=10,
            start_comment_id=comments['items'][-1]['id'],
            extended=1
        )

        # If there are no more comments to fetch, exit the loop
        if len(comments['items']) < 100:
            break

    # print(all_comments.count())

    return [
        {
            'comment_id': str(c['id']),
            'from_id': str(c['from_id']),
            'text': str(c['text']),
            'date': str(c['date']),
            'likes': str(c['likes']['count']) if 'likes' in c else '0',
            'reposts': str(c['thread']['count'])
        }
        for c in all_comments
    ]


def is_promoted_post(post):
    # Проверяем, есть ли в тексте поста значок "Реклама"
    if 'реклама' in str(post['text']).lower():
        return True

    # Проверяем, есть ли в описании вложенной ссылки значок "Реклама"
    if 'attachments' in post and len(post['attachments']) > 0:
        attachment = post['attachments'][0]  # берем только первое вложение
        if attachment['type'] == 'link' and 'link_product' in attachment:
            link_product = attachment['link_product']
            if 'link_title' in link_product and 'link_title' in link_product['link_title']:
                if 'Реклама' in link_product['link_title']['link_title']:
                    return True

    return False



if __name__ == '__main__':
    get_group_posts(group_id_root)
