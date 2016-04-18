# Module for input and output of HomologSet objects
import json
import pickle

from .base import write_to_file, read_from_file
from . import fasta

class Write(object):

    def __init__(self, HomologSet):
        """ Object for writing out metadata held in a HomologSet. """
        self._homologset = HomologSet

    @write_to_file
    def fasta(self, tags=None, aligned=False):
        """ Return string in fasta format for the set."""
        f = ""
        for id, homolog in self._homologset.homologs.items():
            f += homolog.write.fasta(tags, aligned=aligned)
        return f

    @write_to_file
    def phylip(self, alignment_index=0, **kwargs):
        """ Return string of sequences in phylip format. """

        # Get the latest align if other alignment isn't specified
        if alignment_index is 0:
            alignment = "latest_align"
        else:
            alignment = "alignment" + str(alignment_index)

        f = ""
        for id, homolog in self._homologset.homologs.items():
            f += homolog.write.phylip(alignment_index=alignment_index)

        n_homologs = len(self._homologset.homologs)
        n_col = len(getattr(list(self._homologset.homologs.values())[0], alignment_index))

        out = "%i  %i\n\n%s\n" % (n_homologs,n_col,f)
        return out

    @write_to_file
    def json(self, **kwargs):
        """ Return json string of homolog set."""
        obj = list()
        for h in self._homologset.homologs.items():
            obj.append(h.attrs)
        return json.dumps(obj)

    @write_to_file
    def pickle(self, **kwargs):
        """ Return pickle string of homolog set. """
        return pickle.dumps(self._homologset)

    @write_to_file
    def csv(self, tags=None, delimiter=",", **kwargs):
        """ Return csv string. """
        # If tags is not specified, get all tags.
        if tags is None:
            tags = list(list(self._homologset.homologs.values())[0].attrs.keys())

        f = delimiter.join(tags)
        f += "\n"
        for id, homolog in self._homologset.homologs.items():
            f += homolog.write.csv(tags=tags, header=False, delimiter=delimiter)
        return f

    @write_to_file
    def newick(self, tags, **kwargs):
        """ Write a tree to file. """
        old_name = "id"
        new_names = tags
        tree = switch(self._homologset, "id", new_names, format="newick")
        return tree




class Read(object):

    def __init__(self, HomologSet):
        """ """
        self._HomologSet = HomologSet

    @read_from_file
    def fasta(self, data):
        """ """


    @read_from_file
    def newick(self, data):
        pass
