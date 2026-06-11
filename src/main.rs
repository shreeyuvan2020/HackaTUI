use reqwest::Client;
use ratatui_plt::{heatmap_widget, prelude::*};
use ratatui::{Frame, GridData};
use chrono::prelude::*;
async rupub fn spans_data(username:&str) {
    let client = reqwest::Client::new();
    let request = client.get("https://hackatime.hackclub.com/api/v1/users/{username}/heartbeats/spans");
    let response = request.send().await?;
}

fn run(terminal: &mut ratatui::DefaultTerminal) -> std::io::Result<()> {
    loop {
        terminal.draw(|frame| render(frame))?;
        if handle_events()? {
            break Ok(());
        }
    }
}

fn render(frame: &mut Frame) {
    let data = GridData::from_fn((-1.0, 1.0), (-1.0, 1.0), 20, 20, |x, y| x * y);
    let h = heatmap_widget!(data);
    frame.render_widget(h, frame.area());
}