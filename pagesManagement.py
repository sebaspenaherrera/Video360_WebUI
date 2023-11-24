from components.pages.MonitoringVR import get_monitoring_component


# Function for update page's body from the url
def display_monitoring_page(pathname):
    # If the requested page is /monitoring/, create the charts and display them as page content
    if pathname == "/monitoring/":
        return get_monitoring_component()

    # Here we can add additional pages...
