from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

# Load the dataset
df = pd.read_excel("Loki.xlsx")

# Process the dataset and calculate average scores for all POs
results = {}

po_columns = [f"PO{i}" for i in range(1, 13)]

for regno, regno_group in df.groupby("REGNO"):
    po_sum = {po: 0 for po in po_columns}
    co_attainment_count = len(regno_group)
    
    for index, row in regno_group.iterrows():
        for po in po_columns:
            po_sum[po] += row["COATTAINMENT"] * row[po]
    
    po_avgs = {f"{po} Average": round(po_sum[po] / (co_attainment_count * 3), 1) for po in po_columns}
    results[regno] = po_avgs

# PO descriptions
po_descriptions = {
    1: 'ENGINEERING KNOWLEDGE',
    2: 'Problem Analysis',
    3: 'Design/Development of Solutions',
    4: 'Conduct Investigations of Complex Problems',
    5: 'Modern Tool Usage',
    6: 'The Engineer and Society',
    7: 'Environment and Sustainability',
    8: 'Ethics',
    9: 'Individual and Team Work',
    10: 'Communication',
    11: 'Project Management and Finance',
    12: 'Life-long Learning'
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/po_scores', methods=['POST'])
def po_scores():
    regno = request.form['regno']
    regno = int(regno)  # Convert to float
    if regno in results:
        po_scores = results[regno]
        return render_template('po_scores.html', regno=regno, po_scores=po_scores, po_descriptions=po_descriptions)
    else:
        return render_template('not_found.html')

if __name__ == '__main__':
    app.run(debug=True)
