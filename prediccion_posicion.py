import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score
import plotly.express as px
import plotly.graph_objects as go
from sklearn.metrics import confusion_matrix

# Load files
df_completo = pd.read_csv("data_output/datos_jugadores.csv")

# Features selection for the model
features = ["Age", "MarketValue", "goals", "assists", "xG", "xA", "time"]
X = df_completo[features]
y = df_completo["Position"]

# Division in training and test sets with a 20% of data for testing
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

print(f"Training records: {len(X_train)}")
print(f"Test records: {len(X_test)}\n")

# Random Forest training
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Predictions and evaluation
predictions = model.predict(X_test)

print("--- PRECISION REPORT ---")
print(f"General Precision (Accuracy): {accuracy_score(y_test, predictions):.2f}")
print("Details by position:")
print(classification_report(y_test, predictions))

# Test predictions sample
results = X_test.copy()
results["Real_position"] = y_test
results["Predicted_position"] = predictions
print("\n--- TEST COMPARISON ---")
print(results[["goals", "xG", "Real_position", "Predicted_position"]].head())

# Confusion Matrix with Plotly
labels = sorted(y.unique())
cm = confusion_matrix(y_test, predictions, labels=labels)

fig_cm = go.Figure(
    data=go.Heatmap(
        z=cm,
        x=labels,
        y=labels,
        colorscale="Blues",
        text=cm,
        texttemplate="%{text}",
        hovertemplate="Predicted: %{x}<br>Real: %{y}<br>Count: %{z}<extra></extra>",
    )
)

fig_cm.update_layout(
    title="Confusion Matrix: Real vs Predicted Positions",
    xaxis_title="Algorithm predicted position",
    yaxis_title="Real position",
)

fig_cm.write_html("plots_output/confusion_matrix_positions.html")
fig_cm.show()

# 5 Errors Analysis with Plotly
df_errors = X_test.copy()
df_errors["Player"] = df_completo.iloc[X_test.index]["Player"]
df_errors["Real"] = y_test
df_errors["Predicted"] = predictions

# Filter just the first 5 errors
mistakes = df_errors[df_errors["Real"] != df_errors["Predicted"]].head(5)

if mistakes.empty:
    print("The model did not make any errors in the test set.")
else:
    # Plot bar chart for xG, xA, goals
    fig_errors = go.Figure()
    for stat in ["xG", "xA", "goals"]:
        fig_errors.add_trace(go.Bar(x=mistakes["Player"], y=mistakes[stat], name=stat))

    # Add annotations for Real vs Predicted
    for i, row in mistakes.iterrows():
        max_val = max(row["xG"], row["xA"], row["goals"])
        fig_errors.add_annotation(
            x=row["Player"],
            y=max_val + 0.5,
            text=f"Real: {row['Real']}<br>Pred: {row['Predicted']}",
            showarrow=False,
            font=dict(color="red", size=10),
        )

    fig_errors.update_layout(
        title="5 Mistakes: Comparison of xG, xA and Goals",
        yaxis_title="Stats values",
        barmode="group",
    )

    fig_errors.write_html("plots_output/position_prediction_errors.html")
    fig_errors.show()

    print("\n--- Wrong Predictions ---")
    print(mistakes[["Player", "Real", "Predicted", "xG", "xA", "goals"]])
