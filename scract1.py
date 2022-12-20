if show_dogleg:
        trace10 = go.Scatter3d(
        x=df[df['DLS(deg/30m)']<2]['lat'],
        y=df[df['DLS(deg/30m)']<2]['lon'],
        z=df[df['DLS(deg/30m)']<2]['TVD (m RKB)'],
        mode='markers',
        marker=dict(
            color='rgb(128,196,196)',
            size=5
        ),
        name='DLS (°/30m): < 2',
        text = [
                "<b>TVD:</b> {} m<br>"
                "<b>MD:</b> {} m<br>"
                "<b>Inclination:</b> {} °<br>"
                "<b>Azimuth:</b> {} °<br>"
                "<b>DLS:</b> {} °/30m"
                .format(
                        df['TVD (m RKB)'].loc[i],
                        df['MD (m RKB)'].loc[i],
                        df['Inc (deg)'].loc[i],
                        df['Azim (deg)'].loc[i],
                        df['DLS(deg/30m)'].loc[i]
                        )
                for i in df[df['DLS(deg/30m)']<2].index],
        hoverinfo='text'
        )

        trace11 = go.Scatter3d(
        x=df[(df['DLS(deg/30m)']>=2)&(df['DLS(deg/30m)']<4)]['lat'],
        y=df[(df['DLS(deg/30m)']>=2)&(df['DLS(deg/30m)']<4)]['lon'],
        z=df[(df['DLS(deg/30m)']>=2)&(df['DLS(deg/30m)']<4)]['TVD (m RKB)'],
        mode='markers',
        marker=dict(
            color='rgb(0,115,172)',
            size=5
        ),
        name='DLS (°/30m): 2-4',
        text = [
                "<b>TVD:</b> {} m<br>"
                "<b>MD:</b> {} m<br>"
                "<b>Inclination:</b> {} °<br>"
                "<b>Azimuth:</b> {} °<br>"
                "<b>DLS:</b> {} °/30m"
                .format(
                        df['TVD (m RKB)'].loc[i],
                        df['MD (m RKB)'].loc[i],
                        df['Inc (deg)'].loc[i],
                        df['Azim (deg)'].loc[i],
                        df['DLS(deg/30m)'].loc[i]
                        )
                for i in df[(df['DLS(deg/30m)']>=2)&(df['DLS(deg/30m)']<4)].index],
        hoverinfo='text'
        )

        trace12 = go.Scatter3d(
        x=df[(df['DLS(deg/30m)']>=4)&(df['DLS(deg/30m)']<6)]['lat'],
        y=df[(df['DLS(deg/30m)']>=4)&(df['DLS(deg/30m)']<6)]['lon'],
        z=df[(df['DLS(deg/30m)']>=4)&(df['DLS(deg/30m)']<6)]['TVD (m RKB)'],
        mode='markers',
        marker=dict(
            color='rgb(120,123,194)',
            size=5
        ),
        name='DLS (°/30m): 4-6',
        text = [
                "<b>TVD:</b> {} m<br>"
                "<b>MD:</b> {} m<br>"
                "<b>Inclination:</b> {} °<br>"
                "<b>Azimuth:</b> {} °<br>"
                "<b>DLS:</b> {} °/30m"
                .format(
                        df['TVD (m RKB)'].loc[i],
                        df['MD (m RKB)'].loc[i],
                        df['Inc (deg)'].loc[i],
                        df['Azim (deg)'].loc[i],
                        df['DLS(deg/30m)'].loc[i]
                        )
                for i in df[(df['DLS(deg/30m)']>=4)&(df['DLS(deg/30m)']<6)].index],
        hoverinfo='text'
        )

        trace13 = go.Scatter3d(
        x=df[(df['DLS(deg/30m)']>=6)&(df['DLS(deg/30m)']<8)]['lat'],
        y=df[(df['DLS(deg/30m)']>=6)&(df['DLS(deg/30m)']<8)]['lon'],
        z=df[(df['DLS(deg/30m)']>=6)&(df['DLS(deg/30m)']<8)]['TVD (m RKB)'],
        mode='markers',
        marker=dict(
            color='rgb(183,18,124)',
            size=5
        ),
        name='DLS (°/30m): 6-8',
        text = [
                "<b>TVD:</b> {} m<br>"
                "<b>MD:</b> {} m<br>"
                "<b>Inclination:</b> {} °<br>"
                "<b>Azimuth:</b> {} °<br>"
                "<b>DLS:</b> {} °/30m"
                .format(
                        df['TVD (m RKB)'].loc[i],
                        df['MD (m RKB)'].loc[i],
                        df['Inc (deg)'].loc[i],
                        df['Azim (deg)'].loc[i],
                        df['DLS(deg/30m)'].loc[i]
                        )
                for i in df[(df['DLS(deg/30m)']>=6)&(df['DLS(deg/30m)']<8)].index],
        hoverinfo='text'
        )

        trace14 = go.Scatter3d(
        x=df[df['DLS(deg/30m)']>8]['lat'],
        y=df[df['DLS(deg/30m)']>8]['lon'],
        z=df[df['DLS(deg/30m)']>8]['TVD (m RKB)'],
        mode='markers',
        marker=dict(
            color='rgb(204,19,51)',
            size=5
        ),
        name='DLS (°/30m): > 8',
        text = [
                "<b>TVD:</b> {} m<br>"
                "<b>MD:</b> {} m<br>"
                "<b>Inclination:</b> {} °<br>"
                "<b>Azimuth:</b> {} °<br>"
                "<b>DLS:</b> {} °/30m"
                .format(
                        df['TVD (m RKB)'].loc[i],
                        df['MD (m RKB)'].loc[i],
                        df['Inc (deg)'].loc[i],
                        df['Azim (deg)'].loc[i],
                        df['DLS(deg/30m)'].loc[i]
                        )
                for i in df[df['DLS(deg/30m)']>8].index],
        hoverinfo='text'
        )