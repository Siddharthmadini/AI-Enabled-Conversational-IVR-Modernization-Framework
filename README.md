# AI Enabled Conversational IVR Modernization Framework

## Overview

This repository contains the implementation and documentation for the Conversational IVR Modernization Framework internship project.

The project focuses on modernizing legacy VXML-based IVR systems by integrating:
- Azure Communication Services (ACS)
- AI-powered conversational capabilities
- BAP Platform integration

## Project Structure

### Integration Layer (`integration-layer/`)

The integration layer provides the middleware components that bridge legacy IVR systems with modern AI services:

- `main.py` - Main application entry point
- `acs_handler.py` - Azure Communication Services integration
- `ai_connector.py` - AI service connector for conversational capabilities
- `irctc_mock.py` - Mock IRCTC backend for testing
- `middleware.py` - Core middleware logic
- `session_manager.py` - Session state management
- `requirements.txt` - Python dependencies

## Module 1 – Legacy System Analysis

### Scope

- Review legacy VXML-based IVR architecture
- Assess system capabilities
- Identify integration requirements for ACS and BAP
- Analyze technical challenges, constraints, and compatibility gaps

### Legacy System Assumption

The analysis is based on a representative enterprise IVR architecture (Cisco CVP-style VXML execution model) including:

- PSTN call routing
- SIP gateway
- VXML execution engine
- Grammar-based ASR
- Backend REST/SOAP APIs

### Key Gaps Identified

- Grammar-based input vs AI-driven intent detection
- Stateless IVR vs conversational context handling
- Limited streaming capability
- Potential latency from AI processing
- Data format compatibility issues

## Getting Started

1. Install dependencies:
```bash
cd integration-layer
pip install -r requirements.txt
```

2. Run the application:
```bash
python main.py
```

## Module 2 – Integration Layer Implementation

### Overview

The integration layer serves as the middleware between legacy IVR systems and modern AI-powered conversational services. It handles:

- Real-time call management via Azure Communication Services
- AI-driven intent recognition and response generation
- Session state management for conversational context
- Backend system integration (IRCTC mock implementation)

### Architecture

The integration layer follows a modular design:

- **ACS Handler**: Manages Azure Communication Services for call control and media streaming
- **AI Connector**: Interfaces with AI services for natural language understanding and generation
- **Session Manager**: Maintains conversation state and context across interactions
- **Middleware**: Orchestrates data flow between components
- **Backend Integration**: Connects to legacy systems (IRCTC mock for demonstration)

### Features

- Bidirectional streaming for real-time conversation
- Context-aware dialogue management
- Seamless fallback to legacy IVR when needed
- Extensible architecture for additional AI services

## Status

- Module 1: Completed – Legacy System Analysis and Requirements Gathering
- Module 2: In Progress – Integration Layer Implementation
- Integration Layer: Core components implemented

## Documentation

- Module_1_Legacy_System_Analysis_Only.docx — Detailed analysis and integration documentation
