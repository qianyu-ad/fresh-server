from fresh.models.user import db, Admin, User
from fresh.models.topic import (
    Category,
    Tag,
    Like,
    ReadHistory,
    Favorite,
    Article,
    ArticleTagRef,
    Reply
)



def test_data():
    user = User.create(
        id='xxxx',
        name='mink'
    )
    user2 = User.create(
        id='zzzz',
        name='mmi'
    )
    ca = Category.create(name='春季')
    article = Article.create(
        user_id=user.id,
        category_id=ca.id,
        title='春季服装',
        content='好看的服装',
    )
    lks = [
        {
            'user_id': user.id,
            'm_id': article.id,
            'type': Like.TYPE_ARTICLE,
        },
        {
            'user_id': user2.id,
            'm_id': article.id,
            'type': Like.TYPE_ARTICLE,
        }
    ]
    db.session.bulk_insert_mappings(
        Like, lks
    )
    db.session.commit()

    rh = ReadHistory.create(
        user_id=user.id,
        article_id=article.id,
        count=10,
    )
    rh2 = ReadHistory.create(
        user_id=user2.id,
        article_id=article.id,
        count=10,
    )