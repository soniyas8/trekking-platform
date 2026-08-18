from django.test import TestCase
# treks/tests.py
from django.test import TestCase
from .models import Trek
from .route_optimizer import (
    haversine_distance,
    build_distance_matrix,
    route_distance,
    nearest_neighbor_route,
    two_opt,
    optimize_route,
)


class HaversineDistanceTests(TestCase):
    def test_same_point_returns_zero(self):
        """Distance between a point and itself should be 0"""
        distance = haversine_distance(27.9881, 86.9250, 27.9881, 86.9250)
        self.assertEqual(distance, 0)

    def test_known_distance_lukla_to_ebc(self):
        """Straight-line distance from Lukla to Everest Base Camp should be
        roughly 35-40km (shorter than the ~65km trail distance, since this
        is great-circle, not trail, distance)."""
        distance = haversine_distance(27.6866, 86.7314, 28.0025, 86.8528)
        self.assertTrue(35 < distance < 40)

    def test_distance_is_symmetric(self):
        """Distance from A to B should equal distance from B to A"""
        d1 = haversine_distance(28.3949, 83.5866, 27.6866, 86.7314)
        d2 = haversine_distance(27.6866, 86.7314, 28.3949, 83.5866)
        self.assertAlmostEqual(d1, d2, places=5)


class MockTrek:
    """Lightweight stand-in for a Trek object, avoiding DB writes for
    tests that only need latitude/longitude."""
    def __init__(self, name, lat, lon):
        self.name = name
        self.latitude = lat
        self.longitude = lon


class BuildDistanceMatrixTests(TestCase):
    def test_matrix_is_symmetric_and_diagonal_zero(self):
        treks = [
            MockTrek("A", 28.3949, 83.5866),
            MockTrek("B", 27.6866, 86.7314),
            MockTrek("C", 28.1975, 85.3506),
        ]
        matrix = build_distance_matrix(treks)

        # Diagonal should be 0 (distance from a trek to itself)
        for i in range(len(treks)):
            self.assertEqual(matrix[i][i], 0)

        # Matrix should be symmetric
        self.assertAlmostEqual(matrix[0][1], matrix[1][0], places=5)
        self.assertAlmostEqual(matrix[0][2], matrix[2][0], places=5)


class OptimizeRouteTests(TestCase):
    def test_optimize_route_returns_all_treks(self):
        """Optimized route should contain the same treks as the input, just reordered"""
        treks = [
            MockTrek("Annapurna Base Camp", 28.3949, 83.5866),
            MockTrek("Everest Base Camp", 27.6866, 86.7314),
            MockTrek("Langtang Valley Trek", 28.1975, 85.3506),
            MockTrek("Ghorepani Poon Hill Trek", 28.3949, 83.5866),
        ]
        ordered, total_distance = optimize_route(treks)

        self.assertEqual(len(ordered), len(treks))
        self.assertEqual({t.name for t in ordered}, {t.name for t in treks})
        self.assertGreater(total_distance, 0)

    def test_optimize_route_with_single_trek(self):
        """A single trek should return with 0 distance, no crash"""
        treks = [MockTrek("Solo Trek", 28.0, 86.0)]
        ordered, total_distance = optimize_route(treks)

        self.assertEqual(len(ordered), 1)
        self.assertEqual(total_distance, 0.0)

    def test_optimize_route_with_empty_list(self):
        """Empty input should return empty output, no crash"""
        ordered, total_distance = optimize_route([])
        self.assertEqual(ordered, [])
        self.assertEqual(total_distance, 0.0)

    def test_optimize_route_skips_treks_without_coordinates(self):
        """Treks missing lat/long should be excluded, not crash the function"""
        treks = [
            MockTrek("Has Coords", 28.0, 86.0),
            MockTrek("Missing Coords", None, None),
        ]
        ordered, total_distance = optimize_route(treks)

        self.assertEqual(len(ordered), 1)
        self.assertEqual(ordered[0].name, "Has Coords")

    def test_optimize_route_beats_or_matches_naive_order(self):
        """The 2-opt optimized route should never be worse than the
        unoptimized (input) order."""
        treks = [
            MockTrek("Everest Base Camp", 27.6866, 86.7314),
            MockTrek("Annapurna Base Camp", 28.3949, 83.5866),
            MockTrek("Langtang Valley Trek", 28.1975, 85.3506),
            MockTrek("Ghorepani Poon Hill Trek", 28.3949, 83.5866),
        ]
        naive_distance = sum(
            haversine_distance(treks[i].latitude, treks[i].longitude,
                                treks[i + 1].latitude, treks[i + 1].longitude)
            for i in range(len(treks) - 1)
        )
        _, optimized_distance = optimize_route(treks)

        self.assertLessEqual(optimized_distance, naive_distance)


class OptimizeRouteWithRealTrekModelTests(TestCase):
    """One integration-style test using the actual Trek model, to confirm
    the optimizer works with real Django model instances, not just mocks."""

    def setUp(self):
        Trek.objects.create(
            name="Annapurna Base Camp", slug="abc-test",
            description="Test", short_description="Test",
            duration_days=14, difficulty="moderate", max_altitude=4130,
            best_season="March-May", price=1200,
            latitude=28.3949, longitude=83.5866,
        )
        Trek.objects.create(
            name="Everest Base Camp", slug="ebc-test",
            description="Test", short_description="Test",
            duration_days=18, difficulty="difficult", max_altitude=5364,
            best_season="March-May", price=1800,
            latitude=27.6866, longitude=86.7314,
        )

    def test_optimize_route_with_real_treks(self):
        treks = list(Trek.objects.all())
        ordered, total_distance = optimize_route(treks)

        self.assertEqual(len(ordered), 2)
        self.assertGreater(total_distance, 0)
