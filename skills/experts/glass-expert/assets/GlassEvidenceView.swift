// GlassEvidenceView.swift -- verification harness. Renders one glass surface
// and one flat .regularMaterial control side by side over a multi-color
// gradient, so a single on-screen capture carries its own differential
// control: if the two pills look the same, glass is not rendering.
//
// Wire this into a debug window or preview in the target app, capture it on
// screen (scripts/capture_glass_evidence.sh), and judge it against the
// evidence protocol. It is also the known-good baseline when debugging: if
// this harness shows live glass and an app surface does not, the defect is in
// that surface's sampling path, not the environment.

import SwiftUI

@available(macOS 26.0, *)
struct GlassEvidenceView: View {
	var body: some View {
		ZStack {
			// Mid-tone multi-color backdrop: the best judging backdrop.
			// Plain white or black would hide the effect.
			LinearGradient(
				colors: [.orange, .purple, .teal],
				startPoint: .topLeading,
				endPoint: .bottomTrailing
			)
			HStack(spacing: 48) {
				// The surface under test: must show blurred, refracted color.
				Text("glass")
					.padding(24)
					.glassEffect(.regular, in: .rect(cornerRadius: 16))
				// The flat control: must look different from the glass pill.
				Text("control")
					.padding(24)
					.background(.regularMaterial, in: .rect(cornerRadius: 16))
			}
			.font(.title2)
			.foregroundStyle(.primary)
		}
		.frame(width: 520, height: 260)
	}
}
