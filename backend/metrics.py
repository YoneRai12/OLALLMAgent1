"""Prometheus metrics endpoint."""
from __future__ import annotations

from fastapi import APIRouter
from prometheus_client import CollectorRegistry, Gauge, generate_latest

router = APIRouter()
registry = CollectorRegistry()
GPU_UTIL = Gauge('gpu_util', 'GPU utilization', registry=registry)
VRAM = Gauge('gpu_vram_bytes', 'GPU VRAM used', registry=registry)

@router.get('/metrics')
async def metrics() -> bytes:
    # Placeholder values; in real deployment integrate with NVML
    GPU_UTIL.set(0)
    VRAM.set(0)
    return generate_latest(registry)
