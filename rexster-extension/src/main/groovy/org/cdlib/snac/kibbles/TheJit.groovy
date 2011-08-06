package org.cdlib.snac.kibbles;

// The JSON this produces is used by this HMTL/js
// http://code.google.com/p/xtf-cpf/source/browse/cpf2html/snac-jit.html?name=xtf-cpf
// http://code.google.com/p/xtf-cpf/source/browse/cpf2html/snac-jit.js?name=xtf-cpf

import com.tinkerpop.blueprints.pgm.Edge;
import com.tinkerpop.blueprints.pgm.Graph;
import com.tinkerpop.blueprints.pgm.Vertex;
import com.tinkerpop.rexster.extension.*;
import com.tinkerpop.rexster.RexsterResourceContext;
import org.codehaus.jettison.json.JSONObject;
import org.codehaus.jettison.json.JSONArray;
import com.tinkerpop.blueprints.pgm.util.json.JSONWriter;
import com.tinkerpop.gremlin.Gremlin;
import javax.ws.rs.core.Response;

@ExtensionNaming(namespace = "snac", name = "theJit")
public class TheJit extends AbstractRexsterExtension {

    static {
        Gremlin.load();
    }

    @ExtensionDefinition(extensionPoint = ExtensionPoint.VERTEX)
    @ExtensionDescriptor(description = "JSON needed for graphs in the JavaScript InfoVis Toolkit")
    public ExtensionResponse evaluate(@RexsterContext RexsterResourceContext context,
                                      @RexsterContext Vertex v) {

        // JSON format http://thejit.org/static/v20/Docs/files/Loader/Loader-js.html
        JSONArray output = new JSONArray();

        // popular graph neighbors get aggregated into this array
        def neighbors = [];

        // collect neighbors; sorted by "popularity"
        // .score was precomputed with: for (z in g.V ) { z.score = z.out.count() }
        v.out.uniqueObject.sort{-it.score}._()[0..49].aggregate(neighbors)>>-1;

        // add JSON for the "center" node to the output array first
        output.put(buildNode(v, neighbors));

        // for each popular graph neighbor; build neighbors JSON and add to output array
        neighbors.each{ output.put(buildNode(it, neighbors)); }

        // return the results
        return new ExtensionResponse(Response.ok(output).build());
    }

    // build the JSON for the node
    private buildNode(vertex, neighbors) {
        def node = new JSONObject();
        node.put("id", vertex.id as String);
        node.put("name", vertex.identity);
        node.put("adjacencies", buildAdjacencies(vertex, neighbors));
        return node;
    }

    // build array of adjacent nodes
    private buildAdjacencies(vertex, neighbors) {
        JSONArray collect = new JSONArray();
        def self = [];
        vertex._().aggregate(self)>>-1;
        vertex.both.uniqueObject().retain(neighbors).except(self).each {
            collect.put(it.id as String);
        };
        return collect;
    }

}
