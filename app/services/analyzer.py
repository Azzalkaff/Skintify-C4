import json
from pathlib import Path
from typing import Set, List, Dict, Any

class IngredientDatabase:
    """Memuat database bahan skincare dari file JSON lokal."""
    def __init__(self, data_dir: Path):
        self.file_path = data_dir / "ingredient_data.json"
        self.data = {}
        self._load()

    def _load(self):
        if self.file_path.exists():
            try:
                with open(self.file_path, "r", encoding="utf-8") as f:
                    self.data = json.load(f)
            except Exception:
                self.data = {}

    def is_loaded(self) -> bool:
        return bool(self.data)

    def get_aggregate(self, ingredients: Set[str]) -> Dict[str, Any]:
        """Menghitung beban komedogenik/iritasi dari sekumpulan bahan."""
        res = {"comedogenic_rating": 0, "irritant_rating": 0, "active_ingredients": []}
        for ing in ingredients:
            info = self.data.get(ing, {})
            res["comedogenic_rating"] = max(res["comedogenic_rating"], info.get("comedogenic", 0))
            res["irritant_rating"] = max(res["irritant_rating"], info.get("irritation", 0))
            if info.get("is_active"):
                res["active_ingredients"].append(ing)
        return res

class SkincareAnalyzer:
    """Logika deteksi konflik dan rutinitas skincare."""
    
    ACTIVE_INGREDIENTS = {
        "retinol": {"retinol", "retinal", "tretinoin", "adapalene"},
        "aha_bha": {"salicylic acid", "glycolic acid", "lactic acid", "mandelic acid"},
        "vitamin_c": {"ascorbic acid", "l-ascorbic acid", "sodium ascorbyl phosphate"},
        "niacinamide": {"niacinamide"}
    }

    @staticmethod
    def check_routine_safety(ingredients: Set[str]) -> List[str]:
        warnings = []
        has_retinol = any(ing in ingredients for ing in SkincareAnalyzer.ACTIVE_INGREDIENTS["retinol"])
        has_aha_bha = any(ing in ingredients for ing in SkincareAnalyzer.ACTIVE_INGREDIENTS["aha_bha"])
        has_vit_c = any(ing in ingredients for ing in SkincareAnalyzer.ACTIVE_INGREDIENTS["vitamin_c"])

        if has_retinol and has_aha_bha:
            warnings.append("⚠️ Retinol + AHA/BHA: Berisiko iritasi parah dan merusak barrier kulit.")
        if has_vit_c and has_aha_bha:
            warnings.append("⚠️ Vitamin C + AHA/BHA: Dapat menyebabkan ketidakseimbangan pH dan iritasi.")
            
        return warnings

    @staticmethod
    def check_comedogenicity(aggregate: Dict[str, Any]) -> List[str]:
        if aggregate["comedogenic_rating"] >= 4:
            return ["🚫 Rating Komedogenik Tinggi (4-5): Berpotensi menyumbat pori-pori."]
        return []

    @staticmethod
    def check_irritancy_load(aggregate: Dict[str, Any]) -> List[str]:
        if aggregate["irritant_rating"] >= 3:
            return ["⚠️ Beban Iritasi Menengah: Waspada jika kulit Anda sensitif."]
        return []
