#!/usr/bin/env python3
"""
TMA-SRTA Design Validator Tool
Validates Structural Design Pattern Theory implementation accuracy

This tool ensures that TMA implementations correctly adhere to:
1. Four-cause design pattern principles
2. Structural integration requirements
3. Multi-stakeholder principle frameworks
4. Architectural coherence standards
5. Cross-domain applicability patterns

Usage:
    python tools/design_validator.py [directory/file]
    python -m tools.design_validator --comprehensive
"""

import os
import sys
import ast
import json
import argparse
import inspect
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

try:
    from tma.tma_srta import TMAArchitecture, DesignPrinciple, AuthorityModule, InterfaceModule, IntegrationModule
    TMA_AVAILABLE = True
except ImportError:
    TMA_AVAILABLE = False
    print("⚠️  TMA modules not available for runtime validation")


@dataclass
class ValidationIssue:
    """Represents a design pattern validation issue"""
    severity: str  # 'critical', 'warning', 'info'
    category: str  # 'four_cause', 'integration', 'stakeholder', 'architecture'
    message: str
    file_path: Optional[str] = None
    line_number: Optional[int] = None
    suggestion: Optional[str] = None


@dataclass 
class ValidationReport:
    """Complete validation report"""
    timestamp: datetime = field(default_factory=datetime.now)
    target_path: str = ""
    total_files_analyzed: int = 0
    issues: List[ValidationIssue] = field(default_factory=list)
    summary: Dict[str, Any] = field(default_factory=dict)
    recommendations: List[str] = field(default_factory=list)
    
    def add_issue(self, issue: ValidationIssue):
        """Add validation issue to report"""
        self.issues.append(issue)
    
    def get_issues_by_severity(self, severity: str) -> List[ValidationIssue]:
        """Get issues by severity level"""
        return [issue for issue in self.issues if issue.severity == severity]
    
    def get_issues_by_category(self, category: str) -> List[ValidationIssue]:
        """Get issues by category"""
        return [issue for issue in self.issues if issue.category == category]


class DesignPatternValidator:
    """
    Validates Structural Design Pattern Theory implementation
    
    Ensures that code properly implements four-cause design patterns
    and maintains architectural integrity according to SDPT principles.
    """
    
    def __init__(self):
        self.report = ValidationReport()
        self.four_cause_patterns = {
            'material_cause': ['infrastructure', 'data', 'substrate', 'foundation'],
            'formal_cause': ['structure', 'pattern', 'principle', 'constraint', 'authority'],
            'efficient_cause': ['process', 'interface', 'mediation', 'interaction'],
            'final_cause': ['purpose', 'goal', 'integration', 'validation', 'coherence']
        }
        
        self.required_tma_components = {
            'authority_module': ['AuthorityModule', 'principles', 'evaluate_principles'],
            'interface_module': ['InterfaceModule', 'mediate_response', 'transparency'],
            'integration_module': ['IntegrationModule', 'validate_integration', 'coherence']
        }
        
    def validate_directory(self, directory_path: str) -> ValidationReport:
        """Validate all Python files in directory for design pattern compliance"""
        directory = Path(directory_path)
        self.report.target_path = str(directory)
        
        if not directory.exists():
            self.report.add_issue(ValidationIssue(
                severity='critical',
                category='architecture',
                message=f"Target directory not found: {directory_path}"
            ))
            return self.report
        
        python_files = list(directory.rglob("*.py"))
        self.report.total_files_analyzed = len(python_files)
        
        print(f"🔍 Analyzing {len(python_files)} Python files for design pattern compliance...")
        
        for py_file in python_files:
            if self._should_skip_file(py_file):
                continue
                
            try:
                self._validate_file(py_file)
            except Exception as e:
                self.report.add_issue(ValidationIssue(
                    severity='warning',
                    category='architecture',
                    message=f"Could not analyze file: {e}",
                    file_path=str(py_file)
                ))
        
        self._generate_summary()
        self._generate_recommendations()
        return self.report
    
    def validate_file(self, file_path: str) -> ValidationReport:
        """Validate single file for design pattern compliance"""
        file_path = Path(file_path)
        self.report.target_path = str(file_path)
        self.report.total_files_analyzed = 1
        
        if not file_path.exists():
            self.report.add_issue(ValidationIssue(
                severity='critical',
                category='architecture', 
                message=f"Target file not found: {file_path}"
            ))
            return self.report
        
        self._validate_file(file_path)
        self._generate_summary()
        self._generate_recommendations()
        return self.report
    
    def _validate_file(self, file_path: Path):
        """Validate individual file for design pattern implementation"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Parse AST for structural analysis
            try:
                tree = ast.parse(content)
            except SyntaxError as e:
                self.report.add_issue(ValidationIssue(
                    severity='critical',
                    category='architecture',
                    message=f"Syntax error in file: {e}",
                    file_path=str(file_path),
                    line_number=e.lineno
                ))
                return
            
            # Validate different aspects
            self._validate_four_cause_implementation(tree, file_path, content)
            self._validate_tma_architecture(tree, file_path, content)
            self._validate_stakeholder_integration(tree, file_path, content)
            self._validate_design_pattern_consistency(tree, file_path, content)
            
        except Exception as e:
            self.report.add_issue(ValidationIssue(
                severity='warning',
                category='architecture',
                message=f"Error analyzing file: {e}",
                file_path=str(file_path)
            ))
    
    def _validate_four_cause_implementation(self, tree: ast.AST, file_path: Path, content: str):
        """Validate proper four-cause design pattern implementation"""
        class FourCauseVisitor(ast.NodeVisitor):
            def __init__(self, validator):
                self.validator = validator
                self.file_path = file_path
                self.found_causes = set()
                
            def visit_ClassDef(self, node):
                class_name = node.name.lower()
                
                # Check for four-cause pattern implementation
                if 'authority' in class_name or 'principle' in class_name:
                    self.found_causes.add('formal_cause')
                elif 'interface' in class_name or 'mediat' in class_name:
                    self.found_causes.add('efficient_cause')
                elif 'integration' in class_name or 'validat' in class_name:
                    self.found_causes.add('final_cause')
                
                # Validate class has appropriate methods for its cause
                self._validate_class_methods(node)
                self.generic_visit(node)
                
            def _validate_class_methods(self, class_node):
                method_names = [n.name for n in class_node.body if isinstance(n, ast.FunctionDef)]
                class_name = class_node.name.lower()
                
                if 'authority' in class_name:
                    required_methods = ['evaluate_principles', 'extract_constraints']
                    for method in required_methods:
                        if not any(method in m for m in method_names):
                            self.validator.report.add_issue(ValidationIssue(
                                severity='warning',
                                category='four_cause',
                                message=f"Authority class missing expected method pattern: {method}",
                                file_path=str(self.file_path),
                                line_number=class_node.lineno,
                                suggestion=f"Add method containing '{method}' pattern"
                            ))
                
                elif 'interface' in class_name:
                    required_patterns = ['mediate', 'response', 'transparency']
                    missing_patterns = []
                    for pattern in required_patterns:
                        if not any(pattern in m for m in method_names):
                            missing_patterns.append(pattern)
                    
                    if missing_patterns:
                        self.validator.report.add_issue(ValidationIssue(
                            severity='warning',
                            category='four_cause',
                            message=f"Interface class missing method patterns: {missing_patterns}",
                            file_path=str(self.file_path),
                            line_number=class_node.lineno,
                            suggestion="Add methods implementing interface mediation patterns"
                        ))
                
                elif 'integration' in class_name:
                    required_patterns = ['validate', 'coherence', 'integration']
                    missing_patterns = []
                    for pattern in required_patterns:
                        if not any(pattern in m for m in method_names):
                            missing_patterns.append(pattern)
                    
                    if missing_patterns:
                        self.validator.report.add_issue(ValidationIssue(
                            severity='warning', 
                            category='four_cause',
                            message=f"Integration class missing method patterns: {missing_patterns}",
                            file_path=str(self.file_path),
                            line_number=class_node.lineno,
                            suggestion="Add methods implementing integration validation patterns"
                        ))
        
        visitor = FourCauseVisitor(self)
        visitor.visit(tree)
        
        # Check for complete four-cause implementation in TMA files
        if 'tma' in str(file_path).lower() and len(visitor.found_causes) < 3:
            missing_causes = {'formal_cause', 'efficient_cause', 'final_cause'} - visitor.found_causes
            self.report.add_issue(ValidationIssue(
                severity='warning',
                category='four_cause', 
                message=f"TMA file appears to be missing cause implementations: {missing_causes}",
                file_path=str(file_path),
                suggestion="Ensure all four causes are represented in TMA architecture"
            ))
    
    def _validate_tma_architecture(self, tree: ast.AST, file_path: Path, content: str):
        """Validate Three-Module Architecture implementation"""
        class TMAVisitor(ast.NodeVisitor):
            def __init__(self, validator):
                self.validator = validator
                self.file_path = file_path
                self.found_modules = set()
                self.found_integration_patterns = set()
                
            def visit_ClassDef(self, node):
                class_name = node.name
                
                # Check for TMA module classes
                if 'TMAArchitecture' in class_name:
                    self._validate_tma_main_class(node)
                elif 'AuthorityModule' in class_name:
                    self.found_modules.add('authority')
                    self._validate_authority_module(node)
                elif 'InterfaceModule' in class_name:
                    self.found_modules.add('interface')
                    self._validate_interface_module(node)
                elif 'IntegrationModule' in class_name:
                    self.found_modules.add('integration')
                    self._validate_integration_module(node)
                
                self.generic_visit(node)
            
            def _validate_tma_main_class(self, node):
                method_names = [n.name for n in node.body if isinstance(n, ast.FunctionDef)]
                
                required_methods = ['process_with_tma', 'explain_decision']
                for method in required_methods:
                    if method not in method_names:
                        self.validator.report.add_issue(ValidationIssue(
                            severity='critical',
                            category='architecture',
                            message=f"TMAArchitecture missing required method: {method}",
                            file_path=str(self.file_path),
                            line_number=node.lineno,
                            suggestion=f"Implement {method} method for complete TMA functionality"
                        ))
            
            def _validate_authority_module(self, node):
                method_names = [n.name for n in node.body if isinstance(n, ast.FunctionDef)]
                
                if 'evaluate_principles' not in method_names:
                    self.validator.report.add_issue(ValidationIssue(
                        severity='critical',
                        category='architecture',
                        message="AuthorityModule missing evaluate_principles method",
                        file_path=str(self.file_path),
                        line_number=node.lineno
                    ))
            
            def _validate_interface_module(self, node):
                method_names = [n.name for n in node.body if isinstance(n, ast.FunctionDef)]
                
                if 'mediate_response' not in method_names:
                    self.validator.report.add_issue(ValidationIssue(
                        severity='critical',
                        category='architecture',
                        message="InterfaceModule missing mediate_response method", 
                        file_path=str(self.file_path),
                        line_number=node.lineno
                    ))
            
            def _validate_integration_module(self, node):
                method_names = [n.name for n in node.body if isinstance(n, ast.FunctionDef)]
                
                required_methods = ['validate_integration', '_calculate_coherence']
                for method in required_methods:
                    if not any(method in m for m in method_names):
                        self.validator.report.add_issue(ValidationIssue(
                            severity='warning' if method.startswith('_') else 'critical',
                            category='architecture',
                            message=f"IntegrationModule missing {method} method pattern",
                            file_path=str(self.file_path),
                            line_number=node.lineno
                        ))
        
        visitor = TMAVisitor(self)
        visitor.visit(tree)
        
        # Validate interconnected architecture
        if len(visitor.found_modules) >= 2:
            self._validate_module_interconnection(content, file_path)
    
    def _validate_stakeholder_integration(self, tree: ast.AST, file_path: Path, content: str):
        """Validate multi-stakeholder principle integration"""
        if 'stakeholder' not in content.lower() and 'DesignPrinciple' in content:
            self.report.add_issue(ValidationIssue(
                severity='info',
                category='stakeholder',
                message="DesignPrinciple implementation found but no stakeholder integration detected",
                file_path=str(file_path),
                suggestion="Consider adding stakeholder_input parameter to DesignPrinciple instances"
            ))
        
        # Check for proper stakeholder weighting
        class StakeholderVisitor(ast.NodeVisitor):
            def __init__(self, validator):
                self.validator = validator
                self.file_path = file_path
                
            def visit_Call(self, node):
                if (isinstance(node.func, ast.Name) and 
                    node.func.id == 'DesignPrinciple'):
                    
                    # Check if stakeholder_input is provided
                    keyword_names = [kw.arg for kw in node.keywords if kw.arg]
                    
                    if 'stakeholder_input' not in keyword_names:
                        self.validator.report.add_issue(ValidationIssue(
                            severity='warning',
                            category='stakeholder',
                            message="DesignPrinciple without stakeholder_input parameter",
                            file_path=str(self.file_path),
                            line_number=node.lineno,
                            suggestion="Add stakeholder_input parameter for multi-stakeholder support"
                        ))
#!/usr/bin/env python3
"""
TMA-SRTA Design Validator Tool
Validates Structural Design Pattern Theory implementation accuracy

This tool ensures that TMA implementations correctly adhere to:
1. Four-cause design pattern principles
2. Structural integration requirements
3. Multi-stakeholder principle frameworks
4. Architectural coherence standards
5. Cross-domain applicability patterns

Usage:
    python tools/design_validator.py [directory/file]
    python -m tools.design_validator --comprehensive
"""

import os
import sys
import ast
import json
import argparse
import inspect
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

try:
    from tma.tma_srta import TMAArchitecture, DesignPrinciple, AuthorityModule, InterfaceModule, IntegrationModule
    TMA_AVAILABLE = True
except ImportError:
    TMA_AVAILABLE = False
    print("⚠️  TMA modules not available for runtime validation")


@dataclass
class ValidationIssue:
    """Represents a design pattern validation issue"""
    severity: str  # 'critical', 'warning', 'info'
    category: str  # 'four_cause', 'integration', 'stakeholder', 'architecture'
    message: str
    file_path: Optional[str] = None
    line_number: Optional[int] = None
    suggestion: Optional[str] = None


@dataclass 
class ValidationReport:
    """Complete validation report"""
    timestamp: datetime = field(default_factory=datetime.now)
    target_path: str = ""
    total_files_analyzed: int = 0
    issues: List[ValidationIssue] = field(default_factory=list)
    summary: Dict[str, Any] = field(default_factory=dict)
    recommendations: List[str] = field(default_factory=list)
    
    def add_issue(self, issue: ValidationIssue):
        """Add validation issue to report"""
        self.issues.append(issue)
    
    def get_issues_by_severity(self, severity: str) -> List[ValidationIssue]:
        """Get issues by severity level"""
        return [issue for issue in self.issues if issue.severity == severity]
    
    def get_issues_by_category(self, category: str) -> List[ValidationIssue]:
        """Get issues by category"""
        return [issue for issue in self.issues if issue.category == category]


class DesignPatternValidator:
    """
    Validates Structural Design Pattern Theory implementation
    
    Ensures that code properly implements four-cause design patterns
    and maintains architectural integrity according to SDPT principles.
    """
    
    def __init__(self):
        self.report = ValidationReport()
        self.four_cause_patterns = {
            'material_cause': ['infrastructure', 'data', 'substrate', 'foundation'],
            'formal_cause': ['structure', 'pattern', 'principle', 'constraint', 'authority'],
            'efficient_cause': ['process', 'interface', 'mediation', 'interaction'],
            'final_cause': ['purpose', 'goal', 'integration', 'validation', 'coherence']
        }
        

