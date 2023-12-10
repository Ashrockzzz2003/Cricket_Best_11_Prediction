from flask import Flask, jsonify, request
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
import random

app = Flask(__name__)


def build_model_predict_runs(player_name, opposition_team, ground_name):
    final_df = pd.read_csv("data/predict_run_1.csv")
    player_df = final_df[
        [player_name, opposition_team, "Runs", "BF", "Inns", ground_name, "SR"]
    ]

    X = player_df.drop(["Runs"], axis="columns")
    y = player_df["Runs"]
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, shuffle=True
    )

    # Random Forest
    rf_model = RandomForestRegressor()
    rf_model.fit(X_train.values, y_train)

    return rf_model, X_train, X_test, y_train, y_test, player_df


def predict_runs(player_name, opposition_name, ground_name, career_sr):
    try:
        (
            best_model,
            X_train,
            X_test,
            y_train,
            y_test,
            player_df,
        ) = build_model_predict_runs(player_name, opposition_name, ground_name)

        career_BF_avg = max(
            player_df["BF"].mean() + random.randint(-40, 70), player_df["BF"].mean()
        )

        pred_runs = best_model.predict([[1, 1, career_BF_avg, 1, 1, career_sr]])

        return int(pred_runs[0])

    except:
        return -1

def build_bowl_model(player_name, opposition_team, ground_name):
    final_bodf = pd.read_csv("data/predict_economy_1.csv")
    player_bodf = final_bodf[[player_name, opposition_team, ground_name, "overs", "maidens", "runs", "wickets", "economy"]]

    X = player_bodf.drop(["economy"], axis="columns")
    y = player_bodf["economy"]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, shuffle=True)

    # Random Forest
    rf_model = RandomForestRegressor()
    rf_model.fit(X_train.values, y_train)

    return rf_model, X_train, X_test, y_train, y_test, player_bodf

def predict_economy(player_name, opposition_name, ground_name):
    try:
        best_model, X_train, X_test, y_train, y_test, player_bodf = build_bowl_model(player_name, opposition_name, ground_name)
    
        career_overs_avg = max(player_bodf["overs"].mean() + random.randint(-2, 4), player_bodf["overs"].mean())
        career_maidens_avg = max(player_bodf["maidens"].mean() + random.randint(-1, 2), player_bodf["maidens"].mean())
        career_runs_avg = max(player_bodf["runs"].mean() + random.randint(-10, 20), player_bodf["runs"].mean())
        career_wickets_avg = max(player_bodf["wickets"].mean() + random.randint(-1, 2), player_bodf["wickets"].mean())

        # [player_name, opposition_team, ground_name, "overs", "maidens", "runs", "wickets", "economy"]

        predicted_economy = best_model.predict([[1, 1, 1, career_overs_avg, career_maidens_avg, career_runs_avg, career_wickets_avg]])
        
        return round(predicted_economy[0], 2)
    
    except Exception as e:
        # Stack trace print
        print(e.with_traceback())
        return -1

@app.route("/predictRuns/team", methods=["POST"])
def predictRunsTeam():
    if request.method == "POST":
        if request.is_json == False:
            return jsonify({"message": "Invalid JSON"})

        data = request.get_json()

        if "team_name" not in data:
            return jsonify({"message": "Team name not found"})
        if "opposition_name" not in data:
            return jsonify({"message": "Opposition name not found"})
        if "ground_name" not in data:
            return jsonify({"message": "Ground name not found"})

        player_df = pd.read_csv("data/player_data.csv")
        player_df = player_df[player_df["team_name"] == data["team_name"]]

        response_data = []

        for i, row in player_df.iterrows():
            if (
                row["player_role"] == "Bowling Allrounder"
                or row["player_role"] == "Bowler"
            ):
                continue
            player_name = row["player_name"]
            opposition_name = data["opposition_name"]
            ground_name = data["ground_name"]
            career_sr = row["SR"]
            pred_runs = predict_runs(
                player_name, opposition_name, ground_name, career_sr
            )
            response_data.append(
                {"player_name": player_name, "predicted_runs": pred_runs}
            )

        return jsonify({"predicted_data": response_data})
    

@app.route("/predictEconomy/team", methods=["POST"])
def predictEconomyTeam():
    if request.method == "POST":
        if request.is_json == False:
            return jsonify({"message": "Invalid JSON"})

        data = request.get_json()

        if "team_name" not in data:
            return jsonify({"message": "Team name not found"})
        if "opposition_name" not in data:
            return jsonify({"message": "Opposition name not found"})
        if "ground_name" not in data:
            return jsonify({"message": "Ground name not found"})

        player_df = pd.read_csv("data/player_data.csv")
        player_df = player_df[player_df["team_name"] == data["team_name"]]

        response_data = []

        for i, row in player_df.iterrows():
            if row["player_role"] == "Bowling Allrounder" or row['player_role'] == "Bowler" or row['player_role'] == "Allrounder":
                player_name = row["player_name"]
                opposition_name = data["opposition_name"]
                ground_name = data["ground_name"]
                pred_economy = predict_economy(
                    player_name, opposition_name, ground_name
                )
                response_data.append(
                    {"player_name": player_name, "predicted_economy": pred_economy}
                )

        return jsonify({"predicted_data": response_data})


@app.route("/predictRuns/player", methods=["POST"])
def predictRuns():
    if request.method == "POST":
        if request.is_json == False:
            return jsonify({"message": "Invalid JSON"})

        data = request.get_json()

        if "player_name" not in data:
            return jsonify({"message": "Player name not found"})
        if "opposition_name" not in data:
            return jsonify({"message": "Opposition name not found"})
        if "ground_name" not in data:
            return jsonify({"message": "Ground name not found"})
        if "career_sr" not in data:
            return jsonify({"message": "Career strike rate not found"})

        player_name = data["player_name"]
        opposition_name = data["opposition_name"]
        ground_name = data["ground_name"]
        career_sr = data["career_sr"]
        pred_runs = predict_runs(player_name, opposition_name, ground_name, career_sr)
        return jsonify({"predicted_runs": pred_runs})
    

@app.route("/predictEconomy/player", methods=["POST"])
def predictEconomy():
    if request.method == "POST":
        if request.is_json == False:
            return jsonify({"message": "Invalid JSON"})

        data = request.get_json()

        if "player_name" not in data:
            return jsonify({"message": "Player name not found"})
        if "opposition_name" not in data:
            return jsonify({"message": "Opposition name not found"})
        if "ground_name" not in data:
            return jsonify({"message": "Ground name not found"})

        player_name = data["player_name"]
        opposition_name = data["opposition_name"]
        ground_name = data["ground_name"]
        pred_economy = predict_economy(player_name, opposition_name, ground_name)
        return jsonify({"predicted_economy": pred_economy})


@app.route("/runs/allGrounds", methods=["GET"])
def getAllGroundsRuns():
    return jsonify(
        {
            "grounds": [
                "Sharjah",
                "Kuala Lumpur",
                "Bulawayo",
                "Mirpur",
                "Harare",
                "Greater Noida",
                "Belfast",
                "Abu Dhabi",
                "Dubai (DSC)",
                "Dehradun",
                "Edinburgh",
                "Bristol",
                "Cardiff",
                "Taunton",
                "Manchester",
                "Southampton",
                "Leeds",
                "Doha",
                "Chattogram",
                "Pallekele",
                "Hambantota",
                "Colombo (RPS)",
                "Lahore",
                "Dharamsala",
                "Delhi",
                "Chennai",
                "Lucknow",
                "Gros Islet",
                "Dublin",
                "Fatullah",
                "Canberra",
                "Dunedin",
                "Perth",
                "Napier",
                "Sydney",
                "Benoni",
                "Amstelveen",
                "The Hague",
                "Rotterdam",
                "Ayr",
                "Nairobi (Gym)",
                "King City (NW)",
                "Toronto",
                "ICCA Dubai",
                "Gqeberha",
                "Durban",
                "Lord's",
                "Melbourne",
                "Auckland",
                "Brisbane",
                "Adelaide",
                "Hamilton",
                "Birmingham",
                "Eden Gardens",
                "Nagpur",
                "Hobart",
                "Hyderabad",
                "Nottingham",
                "The Oval",
                "Rajkot",
                "Bengaluru",
                "Paarl",
                "Bloemfontein",
                "Mohali",
                "Colombo (PSS)",
                "Colombo (SSC)",
                "Albion",
                "Port of Spain",
                "Castries",
                "Kingston",
                "Indore",
                "Chester-le-Street",
                "Ranchi",
                "Potchefstroom",
                "Bridgetown",
                "Townsville",
                "Cairns",
                "Centurion",
                "Johannesburg",
                "Wankhede",
                "Providence",
                "Basseterre",
                "Dambulla",
                "Cape Town",
                "Visakhapatnam",
                "Wellington",
                "Pune",
                "Jaipur",
                "Kingstown",
                "Bogra",
                "St John's",
                "North Sound",
                "Queenstown",
                "Faisalabad",
                "Multan",
                "Karachi",
                "Darwin",
                "Roseau",
                "Christchurch",
                "Glasgow",
                "Nelson",
                "Dublin (Malahide)",
                "Kimberley",
                "East London",
                "Sylhet",
                "Chelmsford",
                "Khulna",
                "St George's",
                "Aberdeen",
                "Cuttack",
                "Mount Maunganui",
                "Ahmedabad",
                "Kochi",
                "Kanpur",
                "Guwahati",
                "Brabourne",
                "Thiruvananthapuram",
                "Raipur",
                "Tarouba",
                "Vadodara",
                "Deventer",
                "Utrecht",
                "Jamshedpur",
                "Gwalior",
                "Lincoln",
                "Whangarei",
                "Rawalpindi",
                "Galle",
            ]
        }
    )


@app.route("/runs/allOppositions", methods=["GET"])
def getAllOppositionsRuns():
    return {
        "oppositions": [
            "Afghanistan",
            "Australia",
            "Bangladesh",
            "England",
            "India",
            "Netherlands",
            "New Zealand",
            "Pakistan",
            "South Africa",
            "Sri Lanka",
        ]
    }


@app.route("/bowl/allGrounds", methods=["GET"])
def getAllGroundsBowl():
    return {
        "grounds": [
            "Sharjah",
            "Kuala Lumpur",
            "Bulawayo",
            "Mirpur",
            "Harare",
            "Greater Noida",
            "Belfast",
            "Abu Dhabi",
            "Dubai (DSC)",
            "Dehradun",
            "Edinburgh",
            "Bristol",
            "Cardiff",
            "Taunton",
            "Manchester",
            "Southampton",
            "Leeds",
            "Doha",
            "Chattogram",
            "Pallekele",
            "Hambantota",
            "Colombo (RPS)",
            "Lahore",
            "Dharamsala",
            "Delhi",
            "Chennai",
            "Lucknow",
            "Gros Islet",
            "Dublin",
            "Fatullah",
            "ICCA Dubai",
            "Canberra",
            "Dunedin",
            "Perth",
            "Napier",
            "Sydney",
            "Benoni",
            "Amstelveen",
            "The Hague",
            "Rotterdam",
            "Ayr",
            "Nairobi (Gym)",
            "King City (NW)",
            "Toronto",
            "Centurion",
            "Gqeberha",
            "Durban",
            "Lord's",
            "Melbourne",
            "Hobart",
            "Auckland",
            "Brisbane",
            "Adelaide",
            "Hamilton",
            "Birmingham",
            "The Oval",
            "Eden Gardens",
            "Indore",
            "Bengaluru",
            "Nagpur",
            "Hyderabad",
            "Ranchi",
            "Mohali",
            "Nottingham",
            "Wankhede",
            "Rajkot",
            "Paarl",
            "Bloemfontein",
            "Colombo (PSS)",
            "Colombo (SSC)",
            "Albion",
            "Port of Spain",
            "Castries",
            "Kingston",
            "Thiruvananthapuram",
            "Jamshedpur",
            "Ahmedabad",
            "Chester-le-Street",
            "Potchefstroom",
            "Bridgetown",
            "Townsville",
            "Cairns",
            "Visakhapatnam",
            "Johannesburg",
            "Wellington",
            "Providence",
            "Basseterre",
            "Dambulla",
            "Cape Town",
            "Pune",
            "Jaipur",
            "Kingstown",
            "Khulna",
            "Bogra",
            "St John's",
            "North Sound",
            "Queenstown",
            "Faisalabad",
            "Multan",
            "Karachi",
            "Darwin",
            "Roseau",
            "Christchurch",
            "Glasgow",
            "Nelson",
            "Dublin (Malahide)",
            "Kimberley",
            "East London",
            "Sylhet",
            "Chelmsford",
            "St George's",
            "Aberdeen",
            "Cuttack",
            "Mount Maunganui",
            "Kochi",
            "Kanpur",
            "Guwahati",
            "Brabourne",
            "Raipur",
            "Tarouba",
            "Vadodara",
            "Gwalior",
            "Deventer",
            "Utrecht",
            "Lincoln",
            "Whangarei",
            "Rawalpindi",
            "Galle",
        ]
    }

@app.route("/bowl/allOppositions", methods=["GET"])
def getAllOppositionsBowl():
    return {
        "oppositions": [
            "Afghanistan",
            "Australia",
            "Bangladesh",
            "England",
            "India",
            "Netherlands",
            "New Zealand",
            "Pakistan",
            "South Africa",
            "Sri Lanka",
        ]
    }



@app.route("/allPlayers", methods=["GET"])
def getAllPlayers():
    df = pd.read_csv("data/player_data.csv")
    player_data = []
    for i, row in df.iterrows():
        player_data.append(
            {
                "player_name": row["player_name"],
                "player_id": row["player_id"],
                "team_name": row["team_name"],
                "career_sr": row["SR"],
            }
        )

    return jsonify({"player_data": player_data})


if __name__ == "__main__":
    app.run(debug=True)
