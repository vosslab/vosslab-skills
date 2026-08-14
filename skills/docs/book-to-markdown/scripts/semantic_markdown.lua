-- Normalize structured HTML or EPUB content before the GFM writer runs.

function Div(element)
	return element.content
end

function Span(element)
	return element.content
end

function Header(element)
	element.attr = pandoc.Attr()
	return element
end

function Link(element)
	element.attr = pandoc.Attr()
	if #element.content == 0 then
		return {}
	end
	return element
end

function Image(element)
	if #element.caption == 0 then
		return {}
	end
	return element.caption
end

function Figure(element)
	if #element.caption.long > 0 then
		return element.caption.long
	end
	for _, class_name in ipairs(element.classes) do
		if class_name == "wp-block-embed" or class_name == "is-type-video" then
			return {}
		end
	end
	return element.content
end

function RawInline(element)
	local wrapper = element.text:match("^</?figure") or element.text:match("^</?listing")
	if element.format:match("html") and wrapper then
		return {}
	end
	return element
end

function RawBlock(element)
	local wrapper = element.text:match("^</?figure") or element.text:match("^</?listing")
	if element.format:match("html") and wrapper then
		return {}
	end
	return element
end

function CodeBlock(element)
	local language = element.classes[1]
	if language == nil then
		element.attr = pandoc.Attr()
	else
		element.attr = pandoc.Attr("", {language}, {})
	end
	return element
end

function Pandoc(document)
	local title = pandoc.utils.stringify(document.meta.title)
	local shift_value = document.meta["shift-headings"]
	local shift_headings = shift_value ~= nil and pandoc.utils.stringify(shift_value) == "true"
	if shift_headings then
		document = document:walk({
			Header = function(element)
				element.level = math.min(element.level + 1, 6)
				return element
			end
		})
	else
		for index, block in ipairs(document.blocks) do
			if block.t == "Header" and block.level == 1 then
				table.remove(document.blocks, index)
				break
			end
		end
	end
	if title ~= "" then
		for index, block in ipairs(document.blocks) do
			if block.t == "Header" and pandoc.utils.stringify(block.content) == title then
				table.remove(document.blocks, index)
				break
			end
		end
		table.insert(document.blocks, 1, pandoc.Header(1, title))
	end
	local used_levels = {}
	document:walk({
		Header = function(element)
			used_levels[element.level] = true
		end
	})
	local level_map = {}
	local normalized_level = 1
	for level = 1, 6 do
		if used_levels[level] then
			level_map[level] = normalized_level
			normalized_level = normalized_level + 1
		end
	end
	document = document:walk({
		Header = function(element)
			element.level = level_map[element.level]
			return element
		end
	})
	document.meta = {
		author = document.meta.author,
		date = document.meta.date,
		snapshot = document.meta.snapshot,
		source = document.meta.source,
		title = document.meta.title,
	}
	return document
end
