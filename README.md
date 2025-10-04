# Chocolate Quality Control System 🍫

A Python-based automated quality control system for chocolate production that demonstrates Object-Oriented Programming (OOP) principles and design patterns.

## 📋 Table of Contents
- [Overview](#overview)
- [Features](#features)
- [OOP Principles](#oop-principles)
- [Class Diagram](#class-diagram)
- [Installation](#installation)
- [Usage](#usage)
- [Code Structure](#code-structure)
- [Examples](#examples)
- [Technical Details](#technical-details)

## 🎯 Overview

This system simulates an automated quality control process for chocolate manufacturing, featuring defect detection, quality evaluation, and comprehensive reporting. The implementation showcases modern Python programming practices and software design principles.

## ✨ Features

- **Automated Defect Detection** using simulated computer vision
- **Multi-stage Quality Control** for molding and packaging processes
- **Real-time Quality Assessment** with customizable criteria
- **Comprehensive Reporting** with statistics and defect analysis
- **Batch Processing** for high-volume production simulation
- **Interactive Menu System** for easy operation

## 🏗️ OOP Principles

| Principle | Implementation |
|-----------|----------------|
| **Encapsulation** | Protected attributes with getters and private methods |
| **Inheritance** | `MoldedChocolate` and `PackagedChocolate` inherit from base `Chocolate` class |
| **Polymorphism** | Different `evaluate_quality()` implementations for each chocolate type |
| **Abstraction** | `QualitySensor` abstract class with concrete `VisualSensor` implementation |

## 📊 Class Diagram

```mermaid
classDiagram
    class Chocolate {
        -_batch_id: str
        -_production_date: datetime
        -_defects: List[DefectType]
        -_quality_status: QualityStatus
        +batch_id: str
        +defects: List[DefectType]
        +add_defect(defect): None
        +evaluate_quality(): QualityStatus
    }
    
    class MoldedChocolate {
        -_mold_type: str
        +evaluate_quality(): QualityStatus
    }
    
    class PackagedChocolate {
        -_packaging_type: str
        +evaluate_quality(): QualityStatus
    }
    
    class QualitySensor {
        <<abstract>>
        +detect_defects(chocolate): List[DefectType]
    }
    
    class VisualSensor {
        -_analyze_molding(): List[DefectType]
        -_analyze_packaging(): List[DefectType]
        +detect_defects(chocolate): List[DefectType]
    }
    
    class QualityControlSystem {
        -_sensors: Dict[str, QualitySensor]
        -_results: List[Dict]
        +register_sensor(process, sensor): None
        +inspect_chocolate(chocolate, process): QualityStatus
        +generate_report(): str
        +show_inspections(): str
    }
    
    Chocolate <|-- MoldedChocolate
    Chocolate <|-- PackagedChocolate
    QualitySensor <|-- VisualSensor
    QualityControlSystem --> QualitySensor
    QualityControlSystem --> Chocolate# QualitySysteminPOO
