import pandas as pd
import graphlab as gl


def make_factorization_recommender(user_csv_path):
    '''Creates a simple factorization recommender.
    Input: path to CSV
    Output: graphlab model, test rmse score'''

    user_resort_sf = gl.SFrame.read_csv(user_csv_path)
    train_sf, test_sf = gl.recommender.util.random_split_by_user(user_resort_sf, user_id='user_name', item_id='Resort Name', max_num_users=None)

    model = gl.recommender.create(train_sf, target='rating', user_id='user_name', item_id='Resort Name')
    test_rmse = model.evaluate_rmse(test_sf, target='rating')

    return model, test_rmse

def make_content_recommender(user_csv_path, resort_csv_path):
    '''Creates a content-based recommender based on the sub-ratings of the resrots.
    Input: 2 paths to csvs
    Output: graphlab model, test rmse score'''

    user_resort_sf = gl.SFrame.read_csv(user_csv_path)
    resort_ratings_sf = gl.SFrame.read_csv(resort_csv_path)
    train_user, test_user = gl.recommender.util.random_split_by_user(user_resort_sf, user_id='user_name', item_id='Resort Name', max_num_users=None)

    model = gl.recommender.item_content_recommender.create(resort_ratings_sf, 'Resort Name', observation_data=train_user, user_id='user_name', target='rating')

    preds = model.predict(test_user)
    test_rmse = gl.evaluation.rmse(test_user['rating'], preds)
    # test_rmse = model.evaluate_rmse(test_user, target='rating')
    return model, test_rmse


if __name__ == '__main__':
    user_csv_path = 'user_ratings.csv'
    resort_csv_path = 'resort_ratings.csv'
    factorization_model, factor_rmse = make_factorization_recommender(user_csv_path)
    factorization_model.save('models/factorization_model')
    content_model, content_rmse = make_content_recommender(user_csv_path, resort_csv_path)
    # content_model.save('models/content_model')
