use notify::{Watcher, RecursiveMode, watcher};
use std::sync::mpsc::channel;
use std::time::Duration;
use std::process::Command;
use std::fs;

const UPLOAD_DIR: &str = "/path/to/upload_directory";
const RUST_SCRIPT_NAME: &str = "server_migration.rs";

fn main() -> Result<(), Box<dyn std::error::Error>> {
    // Create a channel to receive file change events
    let (sender, receiver) = channel();

    // Start file system watcher
    let mut watcher = watcher(sender, Duration::from_secs(1))?;
    watcher.watch(UPLOAD_DIR, RecursiveMode::NonRecursive)?;

    println!("Monitoring directory for new uploads...");

    loop {
        match receiver.recv() {
            Ok(event) => {
                if let Some(filename) = event.paths.iter().next() {
                    if let Some(file_name) = filename.file_name() {
                        if file_name == RUST_SCRIPT_NAME {
                            // Execute the Rust script
                            println!("Executing the Rust script...");
                            execute_rust_script()?;
                        }
                    }
                }
            }
            Err(e) => {
                eprintln!("Watcher error: {:?}", e);
                break;
            }
        }
    }

    Ok(())
}

fn execute_rust_script() -> Result<(), Box<dyn std::error::Error>> {
    // Compile the Rust script into an executable binary
    let compile_output = Command::new("rustc")
        .arg(RUST_SCRIPT_NAME)
        .output()?;
    
    if !compile_output.status.success() {
        eprintln!("Compilation failed: {:?}", compile_output.stderr);
        return Err("Compilation failed".into());
    }

    // Execute the compiled binary
    let execute_output = Command::new("./server_migration")
        .output()?;
    
    if !execute_output.status.success() {
        eprintln!("Execution failed: {:?}", execute_output.stderr);
        return Err("Execution failed".into());
    }

    Ok(())
}

fn server_migration() {
    // Your server migration logic here
    println!("Executing server migration...");
}