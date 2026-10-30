set part [get_parts xczu5eg-sfvc784-1-e]
puts "FOUND_PART: $part"
set boards [get_board_parts *pynq*]
puts "FOUND_BOARDS: $boards"
set all_zu_boards [get_board_parts *zu*]
puts "FOUND_ZU_BOARDS: $all_zu_boards"
exit 0
