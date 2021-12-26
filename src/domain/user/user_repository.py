from pymongo.collection import Collection
from bson import ObjectId

from src.domain.user.user_entity import UserEntity, UserCollection


class UserRepository:

    def __init__(self, mongodb_user_collection: Collection):
        self.mongodb_user_collection = mongodb_user_collection

    def create(self, user_entity: UserEntity) -> UserEntity:
        insert_one_result = self.mongodb_user_collection.insert_one(user_entity.to_dict())
        return self.fetch(insert_one_result.inserted_id)

    def fetch_all(self) -> UserCollection:
        cursor = self.mongodb_user_collection.find(limit=10)
        return UserCollection.from_mongodb_cursor(cursor)

    def fetch_all_by_account(self, account_id: str):
        cursor = self.mongodb_user_collection.find({'companyId': account_id},limit=10)
        return UserCollection.from_mongodb_cursor(cursor)

    def fetch(self, user_id) -> UserEntity:
        document = self.mongodb_user_collection.find_one({'_id': ObjectId(user_id)})
        if document is None:
            raise UserNotFoundException('user %s not found' % user_id)
        return UserEntity.from_mongodb_document(document)

    def fetch_by_email(self, email) -> UserEntity:
        document = self.mongodb_user_collection.find_one({'email': email})
        if document is None:
            raise UserNotFoundException('user %s not found' % user_id)
        return UserEntity.from_mongodb_document(document)

    def update(self, user_id, user_entity: UserEntity) -> UserEntity:
        update_one_result = self.mongodb_user_collection.update_one({'_id': ObjectId(user_id)},
                                                                    {'$set': user_entity.to_mongodb_document()})
        return self.fetch(user_id)


class UserNotFoundException(Exception):
    def __init__(self, message):
        super(UserNotFoundException, self).__init__(message)
