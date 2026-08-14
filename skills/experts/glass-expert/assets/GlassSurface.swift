// GlassSurface.swift -- drop-in Liquid Glass surface with the layered
// contrast fixes built in. Copy into the target project (the target owns its
// copy) and adjust padding, radius, and defaults. Requires the macOS 26+ SDK.
//
// Encodes three rules so callers cannot get them wrong:
// 1. Reduce Transparency or Increase Contrast -> opaque fill, no glass.
// 2. Optional black scrim between the content and the glass gives text a
//    contrast floor over uncontrolled backdrops (0.4 under white text is
//    roughly 4.6:1 over anything).
// 3. The sampling path below the glass stays clear; the only layer this view
//    inserts under the glass is the intentional scrim.

import SwiftUI

@available(macOS 26.0, *)
struct GlassSurface<Content: View>: View {
	@Environment(\.accessibilityReduceTransparency) private var reduceTransparency
	@Environment(\.colorSchemeContrast) private var contrastScheme

	// Corner radius for the glass shape; the bare glassEffect default is a
	// capsule, so this seed always names its shape explicitly.
	var cornerRadius: CGFloat = 16.0
	// Raise above 0 (for example 0.4) when the surface carries text over a
	// user-controlled backdrop.
	var scrimOpacity: Double = 0.0
	@ViewBuilder var content: () -> Content

	private var needsOpaqueFallback: Bool {
		reduceTransparency || contrastScheme == .increased
	}

	var body: some View {
		if needsOpaqueFallback {
			// Accessibility path: opaque fill, no sampling, full-contrast labels.
			content()
				.background(
					RoundedRectangle(cornerRadius: cornerRadius)
						.fill(.background)
				)
		} else {
			content()
				.background(
					.black.opacity(scrimOpacity),
					in: .rect(cornerRadius: cornerRadius)
				)
				.glassEffect(.regular, in: .rect(cornerRadius: cornerRadius))
		}
	}
}
