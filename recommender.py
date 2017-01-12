import pandas as pd
import graphlab as gl


def make_factorization_recommender():
    '''Creates a simple factorization recommender.
    Input: None
    Output: graphlab model, test rmse score'''

    model = gl.recommender.create(train_sf, target='rating', user_id='user_name', item_id='Resort Name', item_data=resort_ratings_sf)
    test_rmse = model.evaluate_rmse(test_sf, target='rating')

    return model, test_rmse

def make_content_recommender():
    '''Creates a content-based recommender based on the sub-ratings of the resrots.
    Input: None
    Output: graphlab model, test rmse score'''

    model = gl.recommender.item_content_recommender.create(resort_ratings_sf, 'Resort Name', observation_data=user_resort_sf, user_id='user_name', target='rating')

    preds = model.predict(test_sf)
    test_rmse = gl.evaluation.rmse(test_sf['rating'], preds)
    return model, test_rmse


if __name__ == '__main__':
    user_csv_path = 'user_ratings.csv'
    resort_csv_path = 'resort_ratings.csv'

    user_resort_sf = gl.SFrame.read_csv(user_csv_path)
    train_sf, test_sf = gl.recommender.util.random_split_by_user(user_resort_sf, user_id='user_name', item_id='Resort Name', max_num_users=None)
    resort_ratings_sf = gl.SFrame.read_csv(resort_csv_path)

    factorization_model, factor_rmse = make_factorization_recommender()
    factorization_model.save('models/factorization_model')

    content_model, content_rmse = make_content_recommender()
    content_model.save('models/content_model')
