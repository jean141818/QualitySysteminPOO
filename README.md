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



# Create the quality control system
system = QualityControlSystem()

# Register sensors
visual_sensor = VisualSensor()
system.register_sensor("molding", visual_sensor)
system.register_sensor("packaging", visual_sensor)

# Inspect a molded chocolate
chocolate = MoldedChocolate("BATCH-001", datetime.now(), "heart")
result = system.inspect_chocolate(chocolate, "molding")
print(f"Quality Result: {result.value}")
