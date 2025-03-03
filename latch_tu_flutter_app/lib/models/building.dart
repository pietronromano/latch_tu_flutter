import 'package:flutter/material.dart';

enum Buildings {
  northa,
  northb,
  southa,
  southb,
  westa,
  westb,
  easta,
  eastb,
  other
}

class Building {
  const Building(this.title, this.color);

  final String title;
  final Color color;
}
