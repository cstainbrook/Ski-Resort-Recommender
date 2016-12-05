import pandas as pd
import graphlab as gl


def make_factorization_recommender(train_data):
    model = gl.recommender.create(train_data, target='rating', user_id='user_name', item_id='resort_name')
    return model

if __name__ == '__main__':
    user_resort_sf = gl.SFrame.read_csv('user_ratings.csv')
    train_sf, test_sf = gl.recommender.util.random_split_by_user(user_resort_sf, user_id='user_name', item_id='resort_name', max_num_users=None)

    factorization_model = make_factorization_recommender(train_sf)
    test_rmse = factorization_model.evaluate_rmse(test_sf, target='rating')
