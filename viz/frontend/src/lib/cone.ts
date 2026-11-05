/**
 * Swept "cone of uncertainty" (NHC / Windy style): one continuous shape that
 * follows the forecast track and widens with lead time, instead of a separate
 * circle per horizon.
 *
 * Shape = union of the convex hulls of each pair of consecutive circles.
 * Leaflet cannot union polygons, so we return:
 *  - `rings`: the pair hulls, drawn as ONE polygon with fillRule "nonzero"
 *    so overlaps are filled once (uniform tint, no inner lines);
 *  - `outline`: only the hull edges that lie outside every other hull,
 *    drawn as the dashed border.
 * Geometry runs in a local equirectangular km plane (accurate at cone scale).
 */

export type LatLon = [number, number];
export interface ConeNode { lat: number; lon: number; radiusKm: number }

const KM_PER_DEG_LAT = 110.57;
const STEPS = 48; // points per circle

type XY = [number, number];

function hull(points: XY[]): XY[] {
    // Andrew's monotone chain; returns counter-clockwise hull without repeat.
    const p = [...points].sort((a, b) => a[0] - b[0] || a[1] - b[1]);
    const cross = (o: XY, a: XY, b: XY) => (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0]);
    const lower: XY[] = [];
    for (const q of p) {
        while (lower.length >= 2 && cross(lower[lower.length - 2], lower[lower.length - 1], q) <= 0) lower.pop();
        lower.push(q);
    }
    const upper: XY[] = [];
    for (let i = p.length - 1; i >= 0; i--) {
        const q = p[i];
        while (upper.length >= 2 && cross(upper[upper.length - 2], upper[upper.length - 1], q) <= 0) upper.pop();
        upper.push(q);
    }
    return lower.slice(0, -1).concat(upper.slice(0, -1));
}

function inside(pt: XY, ring: XY[]): boolean {
    // Strictly inside a convex CCW ring (small tolerance keeps shared edges "outside").
    for (let i = 0; i < ring.length; i++) {
        const a = ring[i], b = ring[(i + 1) % ring.length];
        if ((b[0] - a[0]) * (pt[1] - a[1]) - (b[1] - a[1]) * (pt[0] - a[0]) <= 1e-6) return false;
    }
    return true;
}

export function sweptCone(nodes: ConeNode[]): { rings: LatLon[][]; outline: LatLon[][] } {
    const valid = nodes.filter((n) => Number.isFinite(n.lat) && Number.isFinite(n.lon) && n.radiusKm > 0);
    if (valid.length === 0) return { rings: [], outline: [] };
    const lat0 = valid[0].lat, lon0 = valid[0].lon;
    const kmPerDegLon = 111.32 * Math.cos((lat0 * Math.PI) / 180);
    const toXY = (lat: number, lon: number): XY => [(lon - lon0) * kmPerDegLon, (lat - lat0) * KM_PER_DEG_LAT];
    const toLL = ([x, y]: XY): LatLon => [lat0 + y / KM_PER_DEG_LAT, lon0 + x / kmPerDegLon];
    const circle = (n: ConeNode): XY[] => {
        const [cx, cy] = toXY(n.lat, n.lon);
        return Array.from({ length: STEPS }, (_, i) => {
            const t = (2 * Math.PI * i) / STEPS;
            return [cx + n.radiusKm * Math.cos(t), cy + n.radiusKm * Math.sin(t)] as XY;
        });
    };
    const circles = valid.map(circle);
    const hulls = circles.length === 1 ? [hull(circles[0])] : circles.slice(1).map((c, i) => hull(circles[i].concat(c)));

    const outline: LatLon[][] = [];
    hulls.forEach((ring, h) => {
        const others = hulls.filter((_, k) => k !== h);
        let run: LatLon[] = [];
        for (let i = 0; i <= ring.length; i++) {
            const pt = ring[i % ring.length];
            if (others.some((o) => inside(pt, o))) {
                if (run.length > 1) outline.push(run);
                run = [];
            } else {
                run.push(toLL(pt));
            }
        }
        if (run.length > 1) outline.push(run);
    });
    return { rings: hulls.map((ring) => ring.map(toLL)), outline };
}
