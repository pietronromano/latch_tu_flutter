import 'package:flutter/material.dart';
import 'package:latch_tu_flutter_app/models/building.dart';

const buildings = {
  Buildings.northa: Building(
    'North A',
    Color.fromARGB(255, 0, 106, 255),
  ),
  Buildings.northb: Building(
    'North B',
    Color.fromARGB(255, 51, 0, 255),
  ),
  Buildings.southa: Building(
    'South A',
    Color.fromARGB(255, 255, 68, 0),
  ),
  Buildings.westa: Building(
    'West A',
    Color.fromARGB(255, 0, 208, 255),
  ),
  Buildings.westb: Building(
    'West B',
    Color.fromARGB(255, 0, 60, 255),
  ),
  Buildings.easta: Building(
    'East A',
    Color.fromARGB(255, 255, 119, 0),
  ),
  Buildings.eastb: Building(
    'East B',
    Color.fromARGB(255, 0, 132, 255),
  ),
  Buildings.other: Building(
    'Other',
    Color.fromARGB(255, 255, 0, 225),
  ),
};
