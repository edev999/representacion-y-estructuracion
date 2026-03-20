import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import confusion_matrix

# Load files
df_stats = pd.read_csv('data_output/datos_jugadores.csv')
df_positions = pd.read_csv('jugadores_combinados.csv')

# Combine datasets
# Using player name as key to merge datasets to add position information to the dataset with xG and xA
df_completo = pd.merge(df_stats, df_positions[['Player', 'Position']], on='Player', how='inner')

# Features selection for the model
features = ['Age', 'MarketValue', 'goals', 'assists', 'xG', 'xA', 'time']
X = df_completo[features]
y = df_completo['Position']

# Division in training and test sets with a 20% of data for testing
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

print(f"Training records: {len(X_train)}")
print(f"Test records: {len(X_test)}\n")

# Random Forest training
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Predictions and evaluation
predictions = model.predict(X_test)

print("--- REPORTE DE PRECISIÓN ---")
print(f"Precisión General (Accuracy): {accuracy_score(y_test, predictions):.2f}")
print("\nDetalle por posición:")
print(classification_report(y_test, predictions))

# Test predictions sample
results = X_test.copy()
results['Real_position'] = y_test
results['Predicted_position'] = predictions
print("\n--- COMPARATIVA EN TEST ---")
print(results[['goals', 'xG', 'Real_position', 'Predicted_position']].head())

# Confusion Matrix
labels = sorted(y.unique())
cm = confusion_matrix(y_test, predictions, labels=labels)

plt.figure(figsize=(8, 6))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
            xticklabels=labels, yticklabels=labels)
plt.title('Confusion Matrix: Real vs Predicted Positions')
plt.xlabel('Algorithm predicted position')
plt.ylabel('Real position')
plt.show()

# 5 erroes analysis
df_errors = X_test.copy()
df_errors['Player'] = df_completo.iloc[X_test.index]['Player']
df_errors['Real'] = y_test
df_errors['Predicted'] = predictions

# Filter just the 5 first errors to analyze
mistakes = df_errors[df_errors['Real'] != df_errors['Predicted']].head(5)

if mistakes.empty:
    print("The model did not make any errors in the test set.")
else:
    # Stats comparison for the 5 errors
    # Shows xG, xA and goals for the 5 players with wrong position prediction
    mistakes.plot(x='Player', y=['xG', 'xA', 'goals'], kind='bar', figsize=(10, 6))
    
    # Add tags with real and predicted position for each player
    for i, (index, row) in enumerate(mistakes.iterrows()):
        plt.text(i, max(row['xG'], row['xA'], row['goals']) + 0.5, 
                 f"Real: {row['Real']}\nPred: {row['Predicted']}", 
                 ha='center', fontsize=9, color='red', fontweight='bold')

    plt.title('5 mistakes: Comparison of xG, xA and goals')
    plt.ylabel('Stats values')
    plt.xticks(rotation=45)
    plt.legend(loc='upper right')
    plt.tight_layout()
    plt.show()

    print("\n--- Wrong Predictions ---")
    print(mistakes[['Player', 'Real', 'Predicted', 'xG', 'xA', 'goals']])