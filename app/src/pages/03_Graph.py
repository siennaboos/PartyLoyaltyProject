import streamlit as st
import plotly.graph_objects as go

# Party data
party_seats = {
    'EPP': 188,
    'S&D': 136,
    'Renew Europe': 77,
    'Greens/EFA': 53,
    'The Left': 46,
    'Patriots for Europe': 84,
    'ECR': 78,
    'ESN': 25,
    'NI': 33
}

# Party colors
party_colors = {
    'EPP': '#0056A0',
    'S&D': '#E60000',
    'Renew Europe': '#009fe3',
    'Greens/EFA': '#54B948',
    'The Left': '#A10000',
    'Patriots for Europe': '#666666',
    'ECR': '#003366',
    'ESN': '#888888',
    'NI': '#444444'
}

st.title("Coalition Builder: Party Leader Dashboard")

# Checkbox party selection
st.write("### Select parties to include in your coalition:")
selected_parties = []
cols = st.columns(3)
for i, (party, seats) in enumerate(party_seats.items()):
    with cols[i % 3]:
        if st.checkbox(f"{party} ({seats})", value=False):
            selected_parties.append(party)

# Seat calculations
selected_seats = sum(party_seats[p] for p in selected_parties)
total_seats = sum(party_seats.values())
majority_needed = 361
missing = max(0, majority_needed - selected_seats)

# Prepare data
labels = selected_parties + ["Remaining"]
values = [party_seats[p] for p in selected_parties] + [total_seats - selected_seats]
colors = [party_colors[p] for p in selected_parties] + ['#DDDDDD']

# Half-donut chart
fig = go.Figure(data=[go.Pie(
    labels=labels,
    values=values,
    hole=0.5,
    direction='clockwise',
    sort=False,
    textinfo='label+value',
    marker=dict(colors=colors),
    showlegend=False
)])

fig.update_traces(
    rotation=180,  # Start from the left (180°)
    domain={'x': [0, 1], 'y': [0.5, 1]}  # Only top half of plot area
)

fig.update_layout(
    height=500,
    width=800,
    margin=dict(t=10, b=10, l=10, r=10),
    annotations=[
        dict(text=f"{selected_seats} / 720<br>Seats", x=0.5, y=0.25, font_size=18, showarrow=False),
        dict(text=f"{missing} to majority", x=0.5, y=0.1, font_size=14, showarrow=False)
    ]
)

st.plotly_chart(fig, use_container_width=True)

# Remaining suggestions
st.markdown("### 🎯 Parties You Haven't Recruited Yet")
if missing > 0:
    remaining_parties = {k: v for k, v in party_seats.items() if k not in selected_parties}
    sorted_parties = sorted(remaining_parties.items(), key=lambda x: x[1], reverse=True)
    for party, seats in sorted_parties:
        st.markdown(f"- **{party}**: {seats} seats — would bring you to {selected_seats + seats} seats")
else:
    st.success("✅ You have a majority coalition!")

st.markdown("---")
st.write("A political group must include at least 23 MEPs elected in at least 7 Member States.")