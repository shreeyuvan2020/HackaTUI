use reqwest::Client;
use ploot::api::quick_heatmap;
use ratatui::{Frame, DefaultTerminal};
use chrono::prelude::*;
use ratatui_plt::{heatmap_widget, prelude::*};
use std::io;
use std::time::Duration;
use color_eyre::eyre::Context;
use color_eyre::Result;
use crossterm::event::{self, KeyCode};
use ratatui::widgets::Paragraph;
async fn spans_data(username:&str) {
    let client = reqwest::Client::new();
    let request = client.get("https://hackatime.hackclub.com/api/v1/users/{username}/heartbeats/spans");
    let response = request.send().await;
}
#[derive(Default)]
pub struct App {
    pub exit: bool,
}

fn main() -> Result<()> {
    color_eyre::install()?; // augment errors / panics with easy to read messages
    ratatui::run(run).context("failed to run app")
}

/// Run the application loop. This is where you would handle events and update the application
/// state. This example exits when the user presses 'q'. Other styles of application loops are
/// possible, for example, you could have multiple application states and switch between them based
/// on events, or you could have a single application state and update it based on events.
fn run(terminal: &mut DefaultTerminal) -> Result<()> {
    loop {
        terminal.draw(render)?;
        if should_quit()? {
            break;
        }
    }
    Ok(())
}

/// Render the application. This is where you would draw the application UI. This example draws a
/// greeting.
fn render(frame: &mut Frame) {
    let data = GridData::from_fn((-1.0, 1.0), (-1.0, 1.0), 20, 20, |x, y| x * y);
    let h = heatmap_widget!(data);
    frame.render_widget(&h, frame.area());
}
fn should_quit() -> Result<bool> {
    if event::poll(Duration::from_millis(250)).context("event poll failed")? {
        let q_pressed = event::read()
            .context("event read failed")?
            .as_key_press_event()
            .is_some_and(|key| key.code == KeyCode::Char('q'));
        return Ok(q_pressed);
    }
    Ok(false)
}