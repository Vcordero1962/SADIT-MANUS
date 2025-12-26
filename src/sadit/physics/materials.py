from dataclasses import dataclass


@dataclass
class MaterialProperties:
    name: str
    youngs_modulus_gpa: float  # Stiffness
    density: float
    citation: str


class MaterialBioMatch:
    """
    Database of material properties for biomechanical matching.
    """

    MATERIALS = {
        "cortical_bone": MaterialProperties("Cortical Bone", 18.0, 1.9, "Rho, Hobatho, Ashman 1993"),
        "cancellous_bone": MaterialProperties("Cancellous Bone", 1.5, 0.9, "Morgan 2003"),
        "titanium_alloy": MaterialProperties("Ti-6Al-4V", 110.0, 4.4, "Standard ASTM F136"),
        "cobalt_chrome": MaterialProperties("Co-Cr-Mo (Austin-Moore)", 220.0, 8.3, "Standard ASTM F75"),
        "stainless_steel": MaterialProperties("316L SS", 193.0, 8.0, "Standard ASTM F138")
    }

    @staticmethod
    def calculate_stiffness_mismatch(material_key: str, bone_key: str = "cortical_bone") -> float:
        """
        Calculates the ratio of Implant Stiffness to Bone Stiffness.
        Ratio > 10 suggests severe Stress Shielding risk.
        """
        mat = MaterialBioMatch.MATERIALS.get(material_key)
        bone = MaterialBioMatch.MATERIALS.get(bone_key)

        if not mat or not bone:
            raise ValueError(f"Unknown material: {material_key} or {bone_key}")

        return mat.youngs_modulus_gpa / bone.youngs_modulus_gpa
