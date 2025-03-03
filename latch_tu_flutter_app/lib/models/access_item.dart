import 'package:latch_tu_flutter_app/models/building.dart';

class AccessItem {
  const AccessItem(
      {required this.id,
      required this.name,
      required this.hours,
      required this.building,
      required this.accountId});

  final String id;
  final String name;
  final int hours;
  final Building building;
  final String accountId;
}
