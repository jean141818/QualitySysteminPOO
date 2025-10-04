from abc import ABC, abstractmethod
from datetime import datetime
from enum import Enum
from typing import List, Dict, Optional

class DefectType(Enum):
    """Enumeration of possible defect types"""
    BUBBLES = "air_bubbles"
    BREAKAGE = "breakage"
    INCORRECT_SHAPE = "incorrect_shape"
    STAINS = "stains"
    MISSING_PIECE = "missing_piece"
    DAMAGED_PACKAGING = "damaged_packaging"

class QualityStatus(Enum):
    """Enumeration of quality statuses"""
    APPROVED = "approved"
    REJECTED = "rejected"
    PENDING = "pending"

class Chocolate:
    """Base class representing a chocolate with its basic attributes"""
    
    def __init__(self, batch_id: str, production_date: datetime):
        self._batch_id = batch_id  # Encapsulation: protected attribute
        self._production_date = production_date
        self._defects: List[DefectType] = []
        self._quality_status = QualityStatus.PENDING
    
    @property
    def batch_id(self) -> str:
        """Getter for batch_id (encapsulation)"""
        return self._batch_id
    
    @property
    def defects(self) -> List[DefectType]:
        """Getter for defects (encapsulation)"""
        return self._defects.copy()  # Return copy to prevent external modification
    
    def add_defect(self, defect: DefectType) -> None:
        """Method to add defects to the chocolate"""
        if defect not in self._defects:
            self._defects.append(defect)
    
    def evaluate_quality(self) -> QualityStatus:
        """Base method for quality evaluation"""
        if not self._defects:
            self._quality_status = QualityStatus.APPROVED
        else:
            self._quality_status = QualityStatus.REJECTED
        return self._quality_status
    
    def __str__(self) -> str:
        return f"Chocolate Batch {self._batch_id} - Status: {self._quality_status.value}"

class MoldedChocolate(Chocolate):
    """Class for chocolates from the molding process (inheritance from Chocolate)"""
    
    def __init__(self, batch_id: str, production_date: datetime, mold_type: str):
        super().__init__(batch_id, production_date)
        self._mold_type = mold_type  # Encapsulation
    
    def evaluate_quality(self) -> QualityStatus:
        """Polymorphism: specific implementation for molding"""
        # Specific molding criteria
        if (DefectType.BUBBLES in self._defects or 
            DefectType.BREAKAGE in self._defects or
            DefectType.INCORRECT_SHAPE in self._defects):
            self._quality_status = QualityStatus.REJECTED
        else:
            self._quality_status = QualityStatus.APPROVED
        return self._quality_status

class PackagedChocolate(Chocolate):
    """Class for chocolates from the packaging process (inheritance from Chocolate)"""
    
    def __init__(self, batch_id: str, production_date: datetime, packaging_type: str):
        super().__init__(batch_id, production_date)
        self._packaging_type = packaging_type
    
    def evaluate_quality(self) -> QualityStatus:
        """Polymorphism: specific implementation for packaging"""
        # Specific packaging criteria
        if (DefectType.BREAKAGE in self._defects or 
            DefectType.DAMAGED_PACKAGING in self._defects or
            DefectType.MISSING_PIECE in self._defects):
            self._quality_status = QualityStatus.REJECTED
        else:
            self._quality_status = QualityStatus.APPROVED
        return self._quality_status

class QualitySensor(ABC):
    """Abstract class for quality sensors (abstraction)"""
    
    @abstractmethod
    def detect_defects(self, chocolate: Chocolate) -> List[DefectType]:
        """Abstract method for defect detection"""
        pass

class VisualSensor(QualitySensor):
    """Visual sensor for defect detection (concrete implementation)"""
    
    def detect_defects(self, chocolate: Chocolate) -> List[DefectType]:
        """Simulates defect detection through computer vision"""
        # In a real implementation, computer vision logic would go here
        detected_defects = []
        
        # Detection simulation (example logic)
        if isinstance(chocolate, MoldedChocolate):
            # Specific logic for molding
            detected_defects.extend(self._analyze_molding())
        
        elif isinstance(chocolate, PackagedChocolate):
            # Specific logic for packaging
            detected_defects.extend(self._analyze_packaging())
        
        return detected_defects
    
    def _analyze_molding(self) -> List[DefectType]:
        """Private method for molding analysis (encapsulation)"""
        # Image analysis simulation
        import random
        possible_defects = [DefectType.BUBBLES, DefectType.BREAKAGE, 
                           DefectType.INCORRECT_SHAPE, DefectType.STAINS]
        return random.choices(possible_defects, k=random.randint(0, 2))
    
    def _analyze_packaging(self) -> List[DefectType]:
        """Private method for packaging analysis (encapsulation)"""
        import random
        possible_defects = [DefectType.BREAKAGE, DefectType.DAMAGED_PACKAGING, 
                           DefectType.MISSING_PIECE]
        return random.choices(possible_defects, k=random.randint(0, 1))

class QualityControlSystem:
    """Main system that manages automated quality control"""
    
    def __init__(self):
        self._sensors: Dict[str, QualitySensor] = {}  # Encapsulation
        self._results: List[Dict] = []
    
    def register_sensor(self, process: str, sensor: QualitySensor) -> None:
        """Registers a sensor for a specific process"""
        self._sensors[process] = sensor
    
    def inspect_chocolate(self, chocolate: Chocolate, process: str) -> QualityStatus:
        """Performs automated inspection of a chocolate"""
        if process not in self._sensors:
            raise ValueError(f"No sensor registered for process: {process}")
        
        sensor = self._sensors[process]
        defects = sensor.detect_defects(chocolate)
        
        # Add detected defects to the chocolate
        for defect in defects:
            chocolate.add_defect(defect)
        
        # Evaluate quality (polymorphism: uses specific implementation)
        result = chocolate.evaluate_quality()
        
        # Register result
        self._register_result(chocolate, defects, result, process)
        
        return result
    
    def _register_result(self, chocolate: Chocolate, defects: List[DefectType], 
                       result: QualityStatus, process: str) -> None:
        """Private method for registering results (encapsulation)"""
        record = {
            'batch_id': chocolate.batch_id,
            'date': datetime.now(),
            'process': process,
            'defects': [d.value for d in defects],
            'result': result.value,
            'chocolate_type': chocolate.__class__.__name__
        }
        self._results.append(record)
    
    def generate_report(self) -> str:
        """Generates a quality report"""
        if not self._results:
            return "No inspection data available to generate report."
        
        total_inspections = len(self._results)
        approved = sum(1 for r in self._results if r['result'] == QualityStatus.APPROVED.value)
        approval_rate = (approved / total_inspections * 100) if total_inspections > 0 else 0
        
        report = f"""
        QUALITY CONTROL REPORT
        ======================
        Total inspections: {total_inspections}
        Approved products: {approved}
        Rejected products: {total_inspections - approved}
        Approval rate: {approval_rate:.2f}%
        
        Defect details:
        """
        
        # Count defects by type
        defect_counter = {}
        for result in self._results:
            for defect in result['defects']:
                defect_counter[defect] = defect_counter.get(defect, 0) + 1
        
        if defect_counter:
            for defect, count in defect_counter.items():
                report += f"  - {defect}: {count} occurrences\n"
        else:
            report += "  No defects detected\n"
        
        return report
    
    def show_inspections(self) -> str:
        """Shows inspection history"""
        if not self._results:
            return "No inspections registered."
        
        report = "INSPECTION HISTORY\n"
        report += "=" * 50 + "\n"
        
        for i, result in enumerate(self._results, 1):
            report += f"{i}. Batch: {result['batch_id']} | "
            report += f"Process: {result['process']} | "
            report += f"Result: {result['result']}\n"
            if result['defects']:
                report += f"   Defects: {', '.join(result['defects'])}\n"
            report += f"   Date: {result['date'].strftime('%Y-%m-%d %H:%M:%S')}\n"
            report += "-" * 50 + "\n"
        
        return report

# Function to display the main menu
def display_menu():
    """Displays the main system menu"""
    print("\n" + "=" * 50)
    print("    CHOCOLATE QUALITY CONTROL SYSTEM")
    print("=" * 50)
    print("1. Inspect molded chocolate")
    print("2. Inspect packaged chocolate")
    print("3. Complete process (molding + packaging)")
    print("4. Generate quality report")
    print("5. Show inspection history")
    print("6. Simulate batch production")
    print("7. Exit")
    print("-" * 50)

# Function to get user input
def get_option():
    """Gets and validates user option"""
    try:
        option = int(input("Select an option (1-7): "))
        return option
    except ValueError:
        print("Error: Please enter a valid number.")
        return -1

# Function to simulate batch production
def simulate_batch_production(system: QualityControlSystem, quantity: int):
    """Simulates production and quality control of multiple chocolates"""
    print(f"\nSimulating production of {quantity} chocolates...")
    
    for i in range(quantity):
        # Create chocolate for molding
        molded_chocolate = MoldedChocolate(f"BATCH-M-{i+1}", datetime.now(), "heart")
        molding_result = system.inspect_chocolate(molded_chocolate, "molding")
        print(f"  Molding {molded_chocolate.batch_id}: {molding_result.value}")
        
        # If molding passes, proceed to packaging
        if molding_result == QualityStatus.APPROVED:
            packaged_chocolate = PackagedChocolate(f"BATCH-P-{i+1}", datetime.now(), "gift_box")
            packaging_result = system.inspect_chocolate(packaged_chocolate, "packaging")
            print(f"  Packaging {packaged_chocolate.batch_id}: {packaging_result.value}")
        else:
            print(f"  ❌ Chocolate {molded_chocolate.batch_id} rejected in molding")

# Main program with interactive menu
def main():
    # Create quality control system
    system = QualityControlSystem()
    
    # Register sensors for each process
    visual_sensor = VisualSensor()
    system.register_sensor("molding", visual_sensor)
    system.register_sensor("packaging", visual_sensor)
    
    print("Quality Control System Initialized")
    print("Sensors registered: Molding and Packaging")
    
    while True:
        display_menu()
        option = get_option()
        
        if option == 1:
            # Inspect molded chocolate
            batch_id = input("Enter batch ID for molding: ")
            chocolate = MoldedChocolate(batch_id, datetime.now(), "heart")
            result = system.inspect_chocolate(chocolate, "molding")
            print(f"\n✅ Result: {result.value}")
            if chocolate.defects:
                print(f"❌ Defects detected: {[d.value for d in chocolate.defects]}")
        
        elif option == 2:
            # Inspect packaged chocolate
            batch_id = input("Enter batch ID for packaging: ")
            chocolate = PackagedChocolate(batch_id, datetime.now(), "gift_box")
            result = system.inspect_chocolate(chocolate, "packaging")
            print(f"\n✅ Result: {result.value}")
            if chocolate.defects:
                print(f"❌ Defects detected: {[d.value for d in chocolate.defects]}")
        
        elif option == 3:
            # Complete process
            batch_id = input("Enter batch ID: ")
            
            # Molding
            molded_chocolate = MoldedChocolate(f"{batch_id}-M", datetime.now(), "heart")
            molding_result = system.inspect_chocolate(molded_chocolate, "molding")
            print(f"\n🔧 Molding: {molding_result.value}")
            
            if molding_result == QualityStatus.APPROVED:
                # Packaging
                packaged_chocolate = PackagedChocolate(f"{batch_id}-P", datetime.now(), "gift_box")
                packaging_result = system.inspect_chocolate(packaged_chocolate, "packaging")
                print(f"📦 Packaging: {packaging_result.value}")
                
                if packaging_result == QualityStatus.APPROVED:
                    print("🎉 Final product APPROVED!")
                else:
                    print("❌ Product rejected in packaging")
            else:
                print("❌ Product rejected in molding")
        
        elif option == 4:
            # Generate report
            print(system.generate_report())
        
        elif option == 5:
            # Show history
            print(system.show_inspections())
        
        elif option == 6:
            # Simulate batch production
            try:
                quantity = int(input("Enter number of chocolates to produce: "))
                if quantity > 0:
                    simulate_batch_production(system, quantity)
                    print(f"\n✅ Simulation completed: {quantity} chocolates processed")
                else:
                    print("❌ Quantity must be greater than 0")
            except ValueError:
                print("❌ Error: Please enter a valid number")
        
        elif option == 7:
            # Exit
            print("\nThank you for using the Quality Control System!")
            break
        
        else:
            print("❌ Invalid option. Please select 1-7.")
        
        input("\nPress Enter to continue...")

if __name__ == "__main__":
    main()