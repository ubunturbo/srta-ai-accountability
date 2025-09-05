"""
TMA-SRTA: Three-Module Architecture for Self-Regulating Transparent AI
Structural Design Pattern Theory (SDPT) implementation

This package implements a novel three-component architecture:
- Authority Module: Core principles and constraints  
- Interface Module: User interaction and mediation
- Integration Module: Monitoring and coherence validation
"""

from .tma_srta import (
    TMAArchitecture,
    AuthorityModule, 
    InterfaceModule,
    IntegrationModule,
    DesignPrinciple,
    ProcessingContext
)

__version__ = "1.0.0"
__all__ = [
    "TMAArchitecture",
    "AuthorityModule", 
    "InterfaceModule", 
    "IntegrationModule",
    "DesignPrinciple",
    "ProcessingContext"
]
