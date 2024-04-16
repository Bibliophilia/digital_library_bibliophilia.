import logging
from typing import Optional

from bibliophilia.users import settings
from bibliophilia.users.domain.boundaries import UserRepository, ReviewRepository
from bibliophilia.users.domain.models.input import UserCreate, ReviewCreate
from fastapi import status

from bibliophilia.users.domain.models.schemas import User, Review


class UserService:
    def __init__(self, user_repository: UserRepository):
        self.repository = user_repository

    def create(self, user: UserCreate) -> Optional[User]:
        user = self.repository.create_user(user)
        return user


class ReviewService:
    def __init__(self, review_repository: ReviewRepository):
        self.review_repository = review_repository

    def create_review(self, review: ReviewCreate) -> (bool, status):
        review = self.review_repository.create_review(review)
        if review:
            logging.info(f"review created: book {review.book_idx}, user {review.user_idx}")
            return True, status.HTTP_201_CREATED
        else:
            return False, status.HTTP_400_BAD_REQUEST

    def read_review(self, book_idx: int, user_idx: str) -> Optional[Review]:
        return self.review_repository.read_review(book_idx, user_idx)

    def read_reviews(self, book_idx: int, page: int) -> list[Review]:
        reviews = self.review_repository.read_reviews(book_idx)
        return reviews[(settings.REVIEWS_IN_PAGE * (page - 1)): (settings.REVIEWS_IN_PAGE * page)]
