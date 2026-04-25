from sklearn.ensemble import RandomForestClassifier
import joblib

# simple manual data (no pandas)
X = [
    [18,1,0,0,1],
    [28,0,1,1,2],
    [19,1,0,0,1],
    [30,0,0,1,2],
    [22,1,0,0,1],
    [35,0,1,1,3]
]

y = [0,1,0,1,0,1]

# model
model = RandomForestClassifier()
model.fit(X, y)

# save
joblib.dump(model, "model.pkl")

print("Model trained successfully!")