from my_library import *

dire = os.listdir("csv")

i = 0
df_list = []
for el in dire:
    df_list.append(pd.read_csv (r'csv/'+el))

trips = df_list[1]['trip_id']


x = np.array(trips)
x_bis = np.unique(x)

create_output(x_bis, df_list)
create_weight_route("output_edges.csv")

create_output_fasce(x_bis, df_list)
create_weight_route("output.csv")

create_file_distance_route(x_bis, df_list)
df = pd.read_csv("output_distance_route.csv")
df = df.drop_duplicates()
df_due = pd.DataFrame(df.groupby(["route"],as_index=False).mean())
df_due.to_csv("route_mean.csv")