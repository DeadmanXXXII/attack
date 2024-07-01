use std::process::Command;
use std::fs;
use std::thread;
use std::time::Duration;
use std::net::{IpAddr, Ipv4Addr};
use log::{info, error};
use notify::{Watcher, RecursiveMode, watcher};

const UPLOAD_DIR: &str = "/path/to/upload_directory";
const CONTAINER_REGISTRY: &str = "container_registry";
const LOG_FILE: &str = "migration.log";

fn main() {
    simple_logging::log_to_file(LOG_FILE, log::LevelFilter::Info).expect("Failed to initialize logger");

    let source_ip = IpAddr::V4(Ipv4Addr::new(192, 168, 1, 50));
    let destination_ip = IpAddr::V4(Ipv4Addr::new(192, 168, 1, 100));

    trigger_migration(source_ip, destination_ip);
}

fn trigger_migration(source_ip: IpAddr, destination_ip: IpAddr) {
    let (tx, rx) = std::sync::mpsc::channel();
    let mut watcher = watcher(tx, Duration::from_secs(1)).expect("Failed to initialize watcher");
    watcher.watch(UPLOAD_DIR, RecursiveMode::Recursive).expect("Failed to watch directory");

    loop {
        match rx.recv() {
            Ok(event) => {
                match event {
                    notify::DebouncedEvent::Create(path) |
                    notify::DebouncedEvent::Write(path) |
                    notify::DebouncedEvent::Rename(_, path) => {
                        if let Some(file_name) = path.file_name() {
                            if let Some(file_name_str) = file_name.to_str() {
                                if file_name_str.ends_with(".rs") {
                                    info!("Triggering migration...");
                                    if let Err(err) = migrate_server(source_ip, destination_ip) {
                                        error!("Migration failed: {}", err);
                                    }
                                }
                            }
                        }
                    }
                    notify::DebouncedEvent::Remove(path) => {
                        if let Some(file_name) = path.file_name() {
                            if let Some(file_name_str) = file_name.to_str() {
                                if file_name_str.ends_with(".rs") {
                                    info!("Triggering migration...");
                                    if let Err(err) = migrate_server(source_ip, destination_ip) {
                                        error!("Migration failed: {}", err);
                                    }
                                }
                            }
                        }
                    }
                    notify::DebouncedEvent::Error(err, _) => {
                        error!("Watcher error: {:?}", err);
                    }
                    _ => {}
                }
            }
            Err(err) => {
                error!("Watcher channel receive error: {:?}", err);
            }
        }
    }
}

fn migrate_server(source_ip: IpAddr, destination_ip: IpAddr) -> Result<(), String> {
    let server_components = identify_server_components()?;
    let container_images = containerize_server_components(&server_components)?;
    synchronize_data(destination_ip)?;
    configure_network(destination_ip)?;
    deploy_containers(&container_images)?;
    validate_migration(destination_ip)?;
    cleanup_source_server()?;

    info!("Server migration completed successfully!");
    Ok(())
}

fn identify_server_components() -> Result<Vec<String>, String> {
    let entries = fs::read_dir(UPLOAD_DIR).map_err(|e| e.to_string())?;
    let mut components = Vec::new();
    for entry in entries {
        let entry = entry.map_err(|e| e.to_string())?;
        let path = entry.path();
        if path.is_file() {
            if let Some(file_name) = path.file_name() {
                if let Some(file_name_str) = file_name.to_str() {
                    if file_name_str.ends_with(".component") {
                        components.push(file_name_str.to_string());
                    }
                }
            }
        }
    }
    if components.is_empty() {
        Err("No server components found.".into())
    } else {
        Ok(components)
    }
}

fn containerize_server_components(components: &[String]) -> Result<Vec<String>, String> {
    let container_images: Vec<String> = components.iter()
        .map(|component| format!("{}/{}", CONTAINER_REGISTRY, component))
        .collect();
    Ok(container_images)
}

fn synchronize_data(destination_ip: IpAddr) -> Result<(), String> {
    let status = Command::new("rsync")
        .arg("-av")
        .arg(UPLOAD_DIR)
        .arg(format!("user@{}:/path/to/destination", destination_ip))
        .status()
        .map_err(|e| e.to_string())?;
    
    if status.success() {
        Ok(())
    } else {
        Err("Data synchronization failed.".into())
    }
}

fn configure_network(destination_ip: IpAddr) -> Result<(), String> {
    let status = Command::new("ssh")
        .arg(format!("user@{}", destination_ip))
        .arg("sudo ifconfig eth0 up")
        .status()
        .map_err(|e| e.to_string())?;
    
    if status.success() {
        Ok(())
    } else {
        Err("Network configuration failed.".into())
    }
}

fn deploy_containers(container_images: &[String]) -> Result<(), String> {
    for image in container_images {
        let status = Command::new("docker")
            .arg("run")
            .arg("-d")
            .arg(image)
            .status()
            .map_err(|e| e.to_string())?;
        
        if !status.success() {
            return Err(format!("Failed to run container image {}", image));
        }
    }
    Ok(())
}

fn validate_migration(destination_ip: IpAddr) -> Result<(), String> {
    let status = Command::new("ssh")
        .arg(format!("user@{}", destination_ip))
        .arg("ping -c 1 8.8.8.8")
        .status()
        .map_err(|e| e.to_string())?;
    
    if status.success() {
        Ok(())
    } else {
        Err("Migration validation failed.".into())
    }
}

fn cleanup_source_server() -> Result<(), String> {
    let status = Command::new("rm")
        .arg("-rf")
        .arg(UPLOAD_DIR)
        .status()
        .map_err(|e| e.to_string())?;
    
    if status.success() {
        Ok(())
    } else {
        Err("Source server cleanup failed.".into())
    }
}
