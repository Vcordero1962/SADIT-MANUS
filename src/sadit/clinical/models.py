from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class PainProfile:
    """
    ALICIA Protocol for Pain Semiology.
    """
    onset: str  # 'sudden', 'gradual' (Aparicion)
    # 'distal', 'inguinal', 'diffuse', 'local_site' (Localizacion)
    location: str
    intensity: int  # 1-10 (Intensidad)
    # 'mechanical', 'inflammatory', 'neuropathic', 'mixed' (Caracter)
    character: str
    irradiation: bool  # True/False
    # ['weight_bearing', 'rest', 'night', 'movement']
    aggravating: List[str] = field(default_factory=list)
    # ['rest', 'medication', 'none']
    alleviating: List[str] = field(default_factory=list)


@dataclass
class LabData:
    """Análisis de laboratorio y marcadores inflamatorios"""
    pcr_level: Optional[float] = None  # mg/L (Proteína C Reactiva)
    # mm/h (Velocidad Sedimentación Globular)
    vsg_level: Optional[float] = None
    wbc_count: Optional[float] = None  # células/μL (Leucocitos)
    hemoglobin: Optional[float] = None  # g/dL
    platelets: Optional[float] = None  # células/μL
    creatinine: Optional[float] = None  # mg/dL

    def has_inflammatory_markers(self) -> bool:
        """Detecta marcadores inflamatorios elevados"""
        inflammatory_pcr = self.pcr_level and self.pcr_level > 10  # Normal <10 mg/L
        inflammatory_vsg = self.vsg_level and self.vsg_level > 20  # Normal <20 mm/h
        leucocitosis = self.wbc_count and self.wbc_count > 11000  # Normal 4000-11000
        return any([inflammatory_pcr, inflammatory_vsg, leucocitosis])


@dataclass
class MedicalHistory:
    """Historia clínica del paciente"""
    antecedentes: List[str] = field(
        default_factory=list)  # ["Diabetes", "HTA", "Obesidad"]
    # ["Metformina", "Enalapril"]
    medicamentos: List[str] = field(default_factory=list)
    # ["Penicilina", "AINEs"]
    alergias: List[str] = field(default_factory=list)
    # ["Artroplastia cadera izq 2015"]
    cirugias_previas: List[str] = field(default_factory=list)


@dataclass
class ClinicalInput:
    pain_profile: PainProfile
    ild_months: int
    mobility_assistance: str
    lab_data: Optional[LabData] = None


@dataclass
class ClinicalInputExtended(ClinicalInput):
    """Entrada clínica extendida para análisis multimodal"""
    medical_history: Optional[MedicalHistory] = None
    imaging_files: List[str] = field(
        default_factory=list)  # Paths a imágenes cargadas
    # Comentarios adicionales del médico
    additional_notes: Optional[str] = None
