#!/usr/bin/env swift
// List on-screen window ids for an app so `screencapture -l <id>` can grab
// the live composited window (offscreen render paths can omit the glass
// backdrop compositing). Run: swift list_window_ids.swift <app-name-substring>

import CoreGraphics
import Foundation

let arguments = CommandLine.arguments
guard arguments.count == 2 else {
	print("usage: swift list_window_ids.swift <app-name-substring>")
	exit(1)
}
let needle = arguments[1].lowercased()

let options: CGWindowListOption = [.optionOnScreenOnly, .excludeDesktopElements]
guard let windowInfo = CGWindowListCopyWindowInfo(options, kCGNullWindowID) as? [[String: Any]] else {
	print("no window information available (check Screen Recording permission)")
	exit(1)
}

var matched = 0
for entry in windowInfo {
	let owner = (entry[kCGWindowOwnerName as String] as? String) ?? ""
	guard owner.lowercased().contains(needle) else { continue }
	let windowID = (entry[kCGWindowNumber as String] as? Int) ?? 0
	let title = (entry[kCGWindowName as String] as? String) ?? ""
	let bounds = (entry[kCGWindowBounds as String] as? [String: Any]) ?? [:]
	let width = (bounds["Width"] as? Int) ?? 0
	let height = (bounds["Height"] as? Int) ?? 0
	print("\(windowID)\t\(owner)\t\(title)\t\(width)x\(height)")
	matched += 1
}

if matched == 0 {
	print("no on-screen windows match: \(needle)")
	exit(1)
}
