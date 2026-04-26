import matplotlib.pyplot as plt
import os
from pyotdr.read import sorparse

TRAZAS_DIR = r"C:\MLpractica3\TRAZAS\Centrales\Chiminangos\CABLE 1"

def generate_plot(id_cable, id_hilo, output_path):
    # Find the sor file
    filename = f"{id_hilo}.sor"
    file_path = os.path.join(TRAZAS_DIR, filename)
    
    if not os.path.exists(file_path):
        # Intentar buscar variaciones del nombre si existe
        files = [f for f in os.listdir(TRAZAS_DIR) if f.startswith(f"{id_hilo}")]
        if files:
            file_path = os.path.join(TRAZAS_DIR, files[0])
        else:
            return None

    status, results, tracedata = sorparse(file_path)
    if status != "ok":
        return None

    if not isinstance(tracedata, list):
        return None

    distances = []
    losses = []
    for line in tracedata:
        try:
            parts = line.strip().split('\t')
            if len(parts) == 2:
                distances.append(float(parts[0]))
                losses.append(float(parts[1]))
        except ValueError:
            pass

    if not distances:
        return None

    plt.figure(figsize=(10, 5))
    plt.plot(distances, losses, color='#00a2e8', linewidth=1.5)
    
    plt.title(f"OTDR Trace - Cable {id_cable}, Hilo {id_hilo}", fontsize=14, pad=15)
    plt.xlabel("Distance (km)", fontsize=12)
    plt.ylabel("Attenuation (dB)", fontsize=12)
    
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.gca().invert_yaxis() # In OTDR plots, usually lower values (more loss) go down, or just regular.
    # Actually OTDR plots show backscatter power (dB) on Y axis. Higher is more power.
    # The data usually shows dB values. Typical OTDR plot has 0 at top and goes down, or just standard.
    # Pyotdr parses it as loss or backscatter. Let's just plot it normally first.
    plt.gca().invert_yaxis() # OTDRs usually have power decreasing downwards.

    # Mark key events if we have them
    key_events = results.get('KeyEvents', {}).get('events', [])
    for ev in key_events:
        dist = float(ev.get('distance', 0))
        plt.axvline(x=dist, color='red', linestyle=':', alpha=0.5)

    plt.tight_layout()
    plt.savefig(output_path, dpi=150)
    plt.close()
    
    return output_path
