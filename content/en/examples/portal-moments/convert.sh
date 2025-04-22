
gsed 's/XYZ(\([0-9]*\),:) *= *\[ *\([0-9.-]*\) *\([0-9.-]*\) *\];/    model.node(\1, (\2, \3))/g' \
  | gsed 's/CON(\([0-9]*\),:) *= *\[ *\([0-9.-]*\) *\([0-9.-]*\) *\];/    model.element(element, \1, (\2, \3), section=section, transform=transform)/g' \
  | gsed 's/^%/    #/g'

