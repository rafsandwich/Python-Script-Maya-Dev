import pymel.core as pm


class CenterJoint:
    def __init__(self):
        pass

    @staticmethod
    def get_skin_cluster(obj):
        for node in pm.listHistory(obj):
            if type(node) == pm.nodetypes.SkinCluster:
                return node

    def to_each(self):
        # TODO Find a way to center a joint in vertex mode
        """
        Centers a joint at each objects you have selected
        """
        # get the selection
        selection = pm.ls(sl=True)

        # clear the selection list
        pm.select(None)

        for poly in selection:
            pm.select(poly)
            cluster = pm.cluster(rel=True)
            pm.select(None)
            joint = pm.joint(n=str(poly + "_jnt"))
            constraint = pm.pointConstraint(cluster, joint)
            pm.delete(constraint, cluster)

    def to_all(self):
        # TODO convert all to vertex, select all and center joint
        """
        Centers a joint to the center of all selected objects
        """
        pass
    def add_and_weight(self, joint, object):
        """
        Adds a joint to the skin cluster and weights
        :param joint:
        :param object:
        :return:
        """
        pass