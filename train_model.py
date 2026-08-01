import pickle
import pandas as pd
from sklearn.linear_model import LinearRegression

def train():
    df = pd.read_csv('data.csv')
    
    x = df[["sqft", "beds"]]
    y = df[["price"]]
    
    model = LinearRegression()
    model.fit(x, y)
    
    with open("model.pkl", "wb") as f:
        pickle.dump(model, f)
        
    print("Model trained and saved as model.pkl")
    
if __name__ == "__main__":
    train()